import os
import streamlit as st
from modules.crewModules import Crews
from modules.chainModules import Chains


## Crew run
crews = Crews()


@st.cache_data(show_spinner=False)
def get_docPath(file, extension_name):
    docPathCrewResult = crews.run_docPathSearch(
        extension_name=extension_name, file_path="./file"
    )
    return docPathCrewResult


@st.cache_data(show_spinner=False)
def get_imgPath(file):
    imgPathCrewResult = crews.run_imgPathSearch(img_path="./file")
    return imgPathCrewResult


@st.cache_data(show_spinner=False)
def get_fileSelect(file, extension_name, keyward, docPaths, imgPaths):
    fileSelectCrewResult = crews.run_fileSelect(keyward, docPaths, imgPaths)
    return fileSelectCrewResult


@st.cache_data(show_spinner=False)
def get_first_answer(question, mainFilePath):
    result = crews.run_questionRespondent(question, mainFilePath)
    return result


@st.cache_data(show_spinner=False)
def get_document_refine_answer(existing_content, relatedFilePaths):
    result = crews.run_document_refine_crew(existing_content, relatedFilePaths)
    return result


@st.cache_data(show_spinner=False)
def get_image_refine_answer(existing_content, imagePaths):
    result = crews.run_image_refine_crew(existing_content, imagePaths)
    return result


@st.cache_data(show_spinner=False)
def get_document_summary(filePath):
    result = crews.run_document_summary_crew(filePath)
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
