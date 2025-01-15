import os
import streamlit as st
import zipfile
from modules.crewModules import Crews
from modules.utilles import paint_history, send_message, clear_session_message
from modules.chainModules import Chains


def preprocess_path(docPathsList, imgPathsList):
    docPaths = []
    imgPaths = []

    for docPath in docPathsList:
        if os.path.isfile(docPath) and os.path.splitext(docPath)[1] == extension_name:
            docPaths.append(docPath)

    for imgPath in imgPathsList:
        if os.path.isfile(imgPath) and os.path.splitext(imgPath)[1] != ".svg":
            imgPaths.append(imgPath)
    return {"docPaths": docPaths, "imgPaths": imgPaths}


@st.dialog("파일 목록", width="large")
def view_all_file_path():
    left, right = st.columns(2, vertical_alignment="top")

    with left:
        st.markdown("### 불러온 문서 목록")
        with st.container(border=True):
            for filePath in st.session_state["searchAllFilePaths"]["docPaths"]:
                file_name = filePath.split("/")[-1]
                st.write(file_name)
    with right:
        st.markdown("### 불러온 이미지 목록")
        with st.container(border=True):
            for imgPath in st.session_state["searchAllFilePaths"]["imgPaths"]:
                img_name = imgPath.split("/")[-1]
                st.write(img_name)


@st.dialog("문서 요약", width="large")
def view_file_summary(file_path):
    with st.spinner("문서를 요약하는 중입니다..."):
        summary_content = get_file_summary(file_path)
    st.markdown("### 요약 내용")
    st.markdown(summary_content)


@st.cache_data(show_spinner=False)
def get_file_summary(file_path):
    chains = Chains()
    result = chains.run_Refine_chain(file_path)
    return result


@st.cache_data(show_spinner=False)
def run_docPathCrew(file, extension_name):
    docPathCrewResult = crews.run_docPathSearch(
        extension_name=extension_name, file_path="./file"
    )
    return docPathCrewResult


@st.cache_data(show_spinner=False)
def run_imgPathCrew(file):
    imgPathCrewResult = crews.run_imgPathSearch(img_path="./file")
    return imgPathCrewResult


@st.cache_data(show_spinner=False)
def run_fileSelectCrew(file, extension_name, keyward, docPaths, imgPaths):
    fileSelectCrewResult = crews.run_fileSelect(keyward, docPaths, imgPaths)
    return fileSelectCrewResult


st.set_page_config(
    page_title="Document J.A.R.V.I.S.",
    page_icon="🖥️",
)

st.title("Document J.A.R.V.I.S.")

st.markdown(
    """
    환영합니다👍\n
    당신이 정리한 문서를 바탕으로 질문에 답을 하고 원하시면 문제도 만들어드릴게요!\n
    '사이드 바'에 정리한 문서들을 Zip 형태로 넣어주세요.\n
    """
)

if "mainFilePath" not in st.session_state:
    st.session_state["mainFilePath"] = False

if "relatedFilePaths" not in st.session_state:
    st.session_state["relatedFilePaths"] = []

if "imagePaths" not in st.session_state:
    st.session_state["imagePaths"] = []

if "isSuccessFile" not in st.session_state:
    st.session_state["isSuccessFile"] = False

if "isLoadFile" not in st.session_state:
    st.session_state["isLoadFile"] = False

if "searchAllFilePaths" not in st.session_state:
    st.session_state["searchAllFilePaths"] = {}

if "associatedFilePaths" not in st.session_state:
    st.session_state["associatedFilePaths"] = {}


with st.sidebar:
    with st.expander("OpenAI API KEY"):
        openAI_API_KEY = st.text_input("OpenAI API KEY 입력")
    file = st.file_uploader("문서 경로를 지정해주세요.", type="zip")
    if st.session_state["isLoadFile"]:
        view_all_file_path_button = st.button("불러온 파일들 보기")
        if view_all_file_path_button:
            if st.session_state["searchAllFilePaths"] == {}:
                st.error("관련된 파일이 존재하지 않습니다..!")
            else:
                view_all_file_path()
        file_reset_button = st.button("파일 경로 RESET")
        if file_reset_button:
            st.session_state["isLoadFile"] = False
            st.cache_data.clear()

    if file:
        with st.spinner(text="In progress..."):
            try:
                zip_file = zipfile.ZipFile(file, "r")
                zip_file.extractall("./file")
                st.session_state["isSuccessFile"] = True
            except:
                st.error(
                    "파일을 Load 할 수 없습니다.\n 올바른 Zip 파일을 불러와주세요."
                )
                st.session_state["isSuccessFile"] = False
                # 구현 해야 됨
    else:
        st.session_state["isSuccessFile"] = False
        st.session_state["isLoadFile"] = False
        st.session_state["searchAllFilePaths"] = {}
        st.session_state["associatedFilePaths"] = {}
        clear_session_message()

if st.session_state["isSuccessFile"]:
    crews = Crews()
    loadFile_tabs, qna_tab, quiz_tabs = st.tabs(
        ["파일 불러오기", "질문하기", "문제 만들기"]
    )

    with loadFile_tabs:
        if st.session_state["isLoadFile"]:
            st.error(
                "이미 파일을 로드하였어요!!\n\n불러온 파일 경로는 수정하시려면 확장자를 변경하거나 '사이드 바'에 있는 버튼을 눌러주세요.\n\n동일 파일 내의 검색을 하길 원하시면 키워드를 바꿔 검색해주세요."
            )
        with st.form("file_option_form"):
            extension_name = st.selectbox(
                "읽을 파일들의 확장자를 선택해주세요.",
                (".pdf", ".txt", ".md", ".docx"),
            )
            keyward = st.text_input(
                "찾고 싶은 키워드를 입력해주세요.",
                placeholder="단어로 입력하면 더 정확하게 찾을 수 있어요!",
            )

            doc_search_button = st.form_submit_button(
                "관련 문서 검색(비용이 발생하니 조심하세요!!)"
            )

            if doc_search_button:
                with st.status("파일을 불러오기...", expanded=True) as status:
                    # 파일 경로 Load
                    with st.spinner(
                        "지정된 경로에 있는 모든 파일을 불러오고 있습니다..."
                    ):
                        docPathCrewResult = run_docPathCrew(file, extension_name)
                    st.write("모든 파일을 불러왔습니다.")

                    with st.spinner(
                        "지정된 경로에 있는 모든 이미지 파일을 불러오고 있습니다..."
                    ):
                        imgPathCrewResult = run_imgPathCrew(file)
                    st.write("모든 이미지를 불러왔습니다.")
                    if docPathCrewResult == "Error" or imgPathCrewResult == "Error":
                        status.update(
                            label="파일을 불러오는데 오류가 발생했습니다.",
                            expanded=False,
                            state="error",
                        )
                    else:
                        # 키워드에 맞는 관련 파일 찾기
                        st.session_state["searchAllFilePaths"] = preprocess_path(
                            docPathCrewResult["filePaths"],
                            imgPathCrewResult["filePaths"],
                        )
                        with st.spinner(
                            "불러온 파일 중 키워드에 맞는 파일들을 찾고 있습니다..."
                        ):
                            fileSelectCrewResult = run_fileSelectCrew(
                                file,
                                extension_name,
                                keyward,
                                st.session_state["searchAllFilePaths"]["docPaths"],
                                st.session_state["searchAllFilePaths"]["imgPaths"],
                            )
                        st.write("키워드에 맞는 파일들을 모두 찾았습니다.")
                        if fileSelectCrewResult == "Error":
                            status.update(
                                label="파일을 불러오는데 오류가 발생했습니다.",
                                expanded=False,
                                state="error",
                            )
                        else:
                            st.session_state["isLoadFile"] = True
                            st.session_state["mainFilePath"] = False
                            st.session_state["relatedFilePaths"] = [
                                False
                                for i in range(
                                    len(fileSelectCrewResult["relatedFilePaths"])
                                )
                            ]
                            st.session_state["imagePaths"] = [
                                False
                                for i in range(len(fileSelectCrewResult["imagePaths"]))
                            ]
                            status.update(label="파일을 불러왔습니다.", expanded=False)
                            st.session_state["associatedFilePaths"] = (
                                fileSelectCrewResult
                            )
                            st.rerun()

        if st.session_state["associatedFilePaths"] != {}:
            st.markdown("## 사용할 문서를 결정해주세요!")
            with st.container(border=True):
                mainFilePath = st.session_state["associatedFilePaths"]["mainFilePath"]
                relatedFilePaths = st.session_state["associatedFilePaths"][
                    "relatedFilePaths"
                ]
                imagePaths = st.session_state["associatedFilePaths"]["imagePaths"]

                # 핵심 문서 경로 설정
                st.markdown("##### 핵심 문서")
                if mainFilePath == "No files are associated." or mainFilePath == []:
                    st.error("문서가 존재하지 않습니다.")
                else:
                    mainFile_name = mainFilePath.split("/")[-1]
                    st.markdown(mainFile_name)
                    st.session_state["mainFilePath"] = mainFilePath
                # 관련 문서 경로 설정
                st.markdown("##### 관련 문서들")
                if relatedFilePaths == []:
                    st.error("문서가 존재하지 않습니다.")
                else:
                    relatedFilePathsToggles = []
                    for relatedFilePath in relatedFilePaths:
                        file_name = relatedFilePath.split("/")[-1]
                        relatedFilePathsToggles.append(st.toggle(file_name))

                    for i, relatedFilePathsToggle in enumerate(relatedFilePathsToggles):
                        if relatedFilePathsToggle:
                            st.session_state["relatedFilePaths"][i] = relatedFilePaths[i]
                        else:
                            st.session_state["relatedFilePaths"][i] = False
                # 이미지 경로 설정
                st.markdown("##### 관련 이미지들")
                if imagePaths == []:
                    st.error("이미지가 존재하지 않습니다.")
                else:
                    imagePathsToggles = []
                    for imagePath in imagePaths:
                        file_name = imagePath.split("/")[-1]
                        imagePathsToggles.append(st.toggle(file_name))

                    for i, imagePathsToggle in enumerate(imagePathsToggles):
                        if imagePathsToggle:
                            st.session_state["imagePaths"][i] = imagePaths[i]
                        else:
                            st.session_state["imagePaths"][i] = False

            st.session_state["mainFilePath"]
            st.session_state["relatedFilePaths"]
            st.session_state["imagePaths"]
    with qna_tab:
        left, mid, right = st.columns(3, vertical_alignment="top")
        isInclude_relatedFiles_toggle = ""
        isInclude_images_toggle = ""

        with left:
            document_summary_button = st.button("문서 전체 요약")
            if document_summary_button:
                view_file_summary(st.session_state["mainFilePath"])

        with mid:
            isInclude_relatedFiles_toggle = st.toggle("관련 문서 포함")

        with right:
            isInclude_images_toggle = st.toggle("관련 이미지 포함")

        response_container = st.container(height=800)
        input_container = st.container()
        chains = Chains()

        if isInclude_images_toggle:
            st.write("관련 이미지를 포함합니다!")

        with response_container:
            paint_history()
        with input_container:
            question = st.chat_input("여기에 물어보고 싶은 내용을 입력해주세요!")
        with response_container:
            if question:
                send_message(question, "human")
                with st.spinner("질문에 대한 답을 만들고 있습니다...."):
                    result = crews.run_questionRespondent(
                        question, st.session_state["mainFilePath"]
                    )

                    if isInclude_relatedFiles_toggle:
                        relatedFilePaths = []
                        for relatedFilePath in st.session_state["relatedFilePaths"]:
                            if relatedFilePath != False:
                                relatedFilePaths.append(relatedFilePath)
                        print(relatedFilePaths)
                        result = crews.run_refine_crew(result, relatedFilePaths)

                    send_message(result, "ai")
