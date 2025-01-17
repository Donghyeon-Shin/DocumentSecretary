import os
import json
import streamlit as st
from modules.crewModules import Crews
from modules.chainModules import Chains


## Data process
def get_file_name(filePath):
    return filePath.split("/")[-1]


def preprocess_path(docPathsList, imgPathsList, extension_name):
    docPaths = []
    imgPaths = []

    for docPath in docPathsList:
        if os.path.isfile(docPath) and os.path.splitext(docPath)[1] == extension_name:
            docPaths.append(docPath)

    for imgPath in imgPathsList:
        if os.path.isfile(imgPath) and os.path.splitext(imgPath)[1] != ".svg":
            imgPaths.append(imgPath)
    return {"docPaths": docPaths, "imgPaths": imgPaths}


def get_file_content(filePath, readMod, encoding, isJson=True):
    try:
        filePathContent = ""
        with open(file=filePath, mode=readMod, encoding=encoding) as f:
            filePathContent = f.read()
        if isJson:
            filePathResultJson = json.loads(filePathContent)
            return filePathResultJson
        else:
            return filePathContent
    except Exception as e:
        print(e)
        return "Error"


## Crew run
crews = Crews()


@st.cache_data(show_spinner=False)
def get_docPath(file, extension_name):
    crews.run_docPathSearch(extension_name=extension_name, file_path="./file")
    filePathResultJson = get_file_content("./docPath.md", "r", "UTF-8")
    if filePathResultJson != "Error":
        filePathsList = filePathResultJson["filePaths"]
        filePaths = []
        for filePath in filePathsList:
            filePaths.append(filePath.replace("\\", "/"))
        result = {"filePaths": filePaths}
        return result
    else:
        return "Error"


@st.cache_data(show_spinner=False)
def get_imgPath(file):
    crews.run_imgPathSearch(img_path="./file")
    filePathResultJson = get_file_content("./ImgPath.md", "r", "UTF-8")
    if filePathResultJson != "Error":
        filePathsList = filePathResultJson["filePaths"]
        filePaths = []
        for filePath in filePathsList:
            filePaths.append(filePath.replace("\\", "/"))
        result = {"filePaths": filePaths}
        return result
    else:
        return "Error"


@st.cache_data(show_spinner=False)
def get_fileSelect(file, extension_name, keyward, docPaths, imgPaths):
    # Path convert to String
    docPathsStr = ""
    docPathsDic = {}
    for docPath in docPaths:
        file_name = get_file_name(docPath)
        docPathsDic.update({file_name: docPath})
        docPathsStr += docPath + "\n"

    imgPathsStr = ""
    imgPathsDic = {}
    for imgPath in imgPaths:
        file_name = get_file_name(imgPath)
        imgPathsDic.update({file_name: imgPath})
        imgPathsStr += imgPath + "\n"

    # Search main file
    crews.run_mainFileSearcher(docPathsStr, keyward)

    mainFileSelectJson = get_file_content("./mainFilePath.md", "r", "UTF-8")
    if mainFileSelectJson == "Error":
        print("mainFileSelectJson")
        return "Error"
    mainFilePath = mainFileSelectJson["mainFile"]

    # Select relevant file
    crews.run_fileSelect(keyward, mainFilePath, docPathsStr, imgPathsStr)

    fileSelectResultJson = get_file_content("./associateFilePath.md", "r", "UTF-8")
    if fileSelectResultJson == "Error":
        print("fileSelectResultJson")
        return "Error"
    relatedFilePathsList = fileSelectResultJson["relatedFiles"]
    imagePathsList = fileSelectResultJson["imageFiles"]

    # relatedFile Paths가 올바르지 않은 경우가 있어, 파일 경로 재설정
    relatedFilePaths = []
    for relatedFilePath in relatedFilePathsList:
        file_name = get_file_name(relatedFilePath)
        if file_name in docPathsDic:
            relatedFilePath = docPathsDic[file_name]
        if (
            os.path.isfile(relatedFilePath)
            and relatedFilePath != mainFilePath
            and not relatedFilePath in relatedFilePaths
        ):
            relatedFilePaths.append(relatedFilePath)

    # Image File 확장자 확인하기(중복으로 사용되어 함수로 만들어 활용해도 될 것 같음.)
    imagePaths = []

    for imgPath in imagePathsList:
        file_name = get_file_name(imgPath)
        if file_name in imgPathsDic:
            imgPath = imgPathsDic[file_name]
        if (
            os.path.isfile(imgPath)
            and os.path.splitext(imgPath)[1] != ".svg"
            and not imgPath in imagePaths
        ):
            imagePaths.append(imgPath)

    result = {
        "mainFilePath": mainFilePath,
        "relatedFilePaths": relatedFilePaths,
        "imagePaths": imagePaths,
    }
    return result


@st.cache_data(show_spinner=False)
def get_first_answer(question, mainFilePath):
    mainDoc = get_file_content(mainFilePath, "r", "UTF-8", False)
    if mainDoc == "Error":
        return "Error"
    result = crews.run_questionRespondent(question, mainDoc)
    return result


@st.cache_data(show_spinner=False)
def get_document_refine_answer(existing_content, relatedFilePaths):
    relatedFileContentList = []
    for relatedFilePath in relatedFilePaths:
        filePathContent = get_file_content(relatedFilePath, "r", "UTF-8", False)
        if filePathContent == "Error":
            return "Error"
        else:
            relatedFileContentList.append(filePathContent)

    result = crews.run_document_refine_crew(existing_content, relatedFileContentList)
    return result


@st.cache_data(show_spinner=False)
def get_image_refine_answer(existing_content, imagePaths):
    result = crews.run_image_refine_crew(existing_content, imagePaths)
    return result


@st.cache_data(show_spinner=False)
def get_document_summary(filePath):
    filePathContent = get_file_content(filePath, "r", "UTF-8", False)
    result = crews.run_document_summary_crew(filePathContent)
    return result


## Chain run
@st.cache_data(show_spinner=False)
def get_file_summary(filePath):
    chains = Chains()
    result = chains.run_Refine_chain(filePath)
    return result


@st.cache_data(show_spinner=False)
def get_question_formmat(filePath):
    chains = Chains()
    result = chains.run_quiz_chain(filePath)
    return result


if "messages" not in st.session_state:
    st.session_state["messages"] = []


def paint_history():
    for message in st.session_state["messages"]:
        send_message(message["message"], message["role"], False)


def save_message(message, role):
    st.session_state["messages"].append({"message": message, "role": role})


def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
        if save:
            save_message(message, role)


def clear_session_message():
    st.session_state["messages"] = []
