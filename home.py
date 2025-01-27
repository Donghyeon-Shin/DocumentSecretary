import pysqlite3 as sqlite3

__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
import time
import streamlit as st
import zipfile
from modules.utilles import (
    paint_history,
    paint_error,
    send_message,
    clear_session_message,
    preprocess_path,
    get_file_name,
    get_docPath,
    get_imgPath,
    get_fileSelect,
    get_first_answer,
    get_document_refine_answer,
    get_image_refine_answer,
    get_document_summary,
    get_quiz_json,
)


## Session Difinition
if "mainFilePath" not in st.session_state:
    st.session_state["mainFilePath"] = ""

if "chosenRelatedFilePaths" not in st.session_state:
    st.session_state["chosenRelatedFilePaths"] = []

if "chosenImagePaths" not in st.session_state:
    st.session_state["chosenImagePaths"] = []

if "isSuccessFile" not in st.session_state:
    st.session_state["isSuccessFile"] = False

if "isLoadFile" not in st.session_state:
    st.session_state["isLoadFile"] = False

if "searchAllFilePaths" not in st.session_state:
    st.session_state["searchAllFilePaths"] = {}

if "associatedFilePaths" not in st.session_state:
    st.session_state["associatedFilePaths"] = {}

if "start_status" not in st.session_state:
    st.session_state["start_status"] = False

if "quiz_json" not in st.session_state:
    st.session_state["quiz_json"] = {}

if "quiz_change_value" not in st.session_state:
    st.session_state["quiz_change_value"] = 0

## Page title, Header setting
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


## Dialog
@st.dialog("파일 목록", width="large")
def view_all_file_path():
    left, right = st.columns(2, vertical_alignment="top")

    with left:
        st.markdown("### 불러온 문서 목록")
        with st.container(border=True):
            for filePath in st.session_state["searchAllFilePaths"]["docPaths"]:
                file_name = get_file_name(filePath)
                st.write(file_name)
    with right:
        st.markdown("### 불러온 이미지 목록")
        with st.container(border=True):
            for imgPath in st.session_state["searchAllFilePaths"]["imgPaths"]:
                img_name = get_file_name(imgPath)
                st.write(img_name)


@st.dialog("문서 요약", width="large")
def view_file_summary(file_path):
    with st.spinner("문서를 요약하는 중입니다..."):
        # summary_content = get_file_summary(file_path)
        summary_content = get_document_summary(file_path, openAI_API_KEY)
    st.markdown("### 요약 내용")
    st.markdown(summary_content)


## Side bar
with st.sidebar:
    with st.expander("OpenAI API KEY"):
        openAI_API_KEY = st.text_input("OpenAI API KEY 입력")
    file = st.file_uploader("문서 경로를 지정해주세요.", type="zip")
    if st.session_state["isLoadFile"]:
        view_all_file_path_button = st.button("불러온 파일들 보기")
        if view_all_file_path_button:
            if st.session_state["searchAllFilePaths"] == {}:
                paint_error("관련된 파일이 존재하지 않습니다..!")
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
                paint_error(
                    "파일을 Load 할 수 없습니다.\n 올바른 Zip 파일을 불러와주세요."
                )
                st.session_state["isSuccessFile"] = False
                # 구현 해야 됨
    else:
        st.session_state["isSuccessFile"] = False
        st.session_state["isLoadFile"] = False
        st.session_state["searchAllFilePaths"] = {}
        st.session_state["associatedFilePaths"] = {}
        st.session_state["start_status"] = False
        st.session_state["quiz_json"] = {}
        st.session_state["quiz_change_value"] = 0
        clear_session_message()

## Main content
if st.session_state["isSuccessFile"] and openAI_API_KEY.startswith("sk-"):
    loadFile_tabs, qna_tab, quiz_tabs = st.tabs(
        ["파일 불러오기", "질문하기", "문제 만들기"]
    )

    ## Load file tab
    with loadFile_tabs:
        if st.session_state["isLoadFile"]:
            paint_error(
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
                    isSuccessLoadDocPath = False
                    isSuccessLoadImagPath = False
                    isSuccessSelectFile = False
                    # 파일 경로 Load
                    with st.spinner(
                        "지정된 경로에 있는 모든 파일을 불러오고 있습니다..."
                    ):
                        docPathCrewResult = get_docPath(
                            file,
                            extension_name,
                            openAI_API_KEY,
                        )
                        if docPathCrewResult == "Error":
                            status.update(
                                label="파일을 불러오는데 오류가 발생했습니다.",
                                expanded=False,
                                state="error",
                            )
                        else:
                            isSuccessLoadDocPath = True
                            st.write("모든 파일을 불러왔습니다.")

                    if isSuccessLoadDocPath:
                        with st.spinner(
                            "지정된 경로에 있는 모든 이미지 파일을 불러오고 있습니다..."
                        ):
                            imgPathCrewResult = get_imgPath(file, openAI_API_KEY)
                        if imgPathCrewResult == "Error":
                            status.update(
                                label="파일을 불러오는데 오류가 발생했습니다.",
                                expanded=False,
                                state="error",
                            )
                        else:
                            isSuccessLoadImagPath = True
                            st.write("모든 이미지를 불러왔습니다.")
                    if isSuccessLoadImagPath:
                        # 키워드에 맞는 관련 파일 찾기
                        with st.spinner(
                            "불러온 파일 중 키워드에 맞는 파일들을 찾고 있습니다..."
                        ):

                            st.session_state["searchAllFilePaths"] = preprocess_path(
                                docPathCrewResult["filePaths"],
                                imgPathCrewResult["filePaths"],
                                extension_name=extension_name,
                            )
                            fileSelectCrewResult = get_fileSelect(
                                file,
                                extension_name,
                                keyward,
                                st.session_state["searchAllFilePaths"]["docPaths"],
                                st.session_state["searchAllFilePaths"]["imgPaths"],
                                openAI_API_KEY,
                            )
                        if fileSelectCrewResult == "Error":
                            status.update(
                                label="파일을 불러오는데 오류가 발생했습니다.",
                                expanded=False,
                                state="error",
                            )
                        else:
                            st.write("키워드에 맞는 파일들을 모두 찾았습니다.")
                            isSuccessSelectFile = True
                            st.session_state["isLoadFile"] = True
                            st.session_state["mainFilePath"] = ""
                            st.session_state["chosenRelatedFilePaths"] = [
                                False
                                for i in range(
                                    len(fileSelectCrewResult["relatedFilePaths"])
                                )
                            ]
                            st.session_state["chosenImagePaths"] = [
                                False
                                for i in range(len(fileSelectCrewResult["imagePaths"]))
                            ]
                            status.update(
                                label="파일을 불러왔습니다.",
                                expanded=False,
                            )
                            st.session_state["associatedFilePaths"] = (
                                fileSelectCrewResult
                            )
                            st.rerun()

        # Path selection options setting
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
                    paint_error("문서가 존재하지 않습니다.")
                else:
                    mainFileName = get_file_name(mainFilePath)
                    st.markdown(mainFileName)
                    st.session_state["mainFilePath"] = mainFilePath
                # 관련 문서 경로 설정
                st.markdown("##### 관련 문서들")
                if relatedFilePaths == []:
                    paint_error("문서가 존재하지 않습니다.")
                else:
                    relatedFilePathsToggles = []
                    for relatedFilePath in relatedFilePaths:
                        relatedFileName = get_file_name(relatedFilePath)
                        relatedFilePathsToggles.append(st.toggle(relatedFileName))

                    for i, relatedFilePathsToggle in enumerate(relatedFilePathsToggles):
                        if relatedFilePathsToggle:
                            st.session_state["chosenRelatedFilePaths"][i] = (
                                relatedFilePaths[i]
                            )
                        else:
                            st.session_state["chosenRelatedFilePaths"][i] = False
                # 이미지 경로 설정
                st.markdown("##### 관련 이미지들")
                if imagePaths == []:
                    paint_error("이미지가 존재하지 않습니다.")
                else:
                    imagePathsToggles = []
                    for imagePath in imagePaths:
                        imageFileName = get_file_name(imagePath)
                        imagePathsToggles.append(st.toggle(imageFileName))

                    for i, imagePathsToggle in enumerate(imagePathsToggles):
                        if imagePathsToggle:
                            st.session_state["chosenImagePaths"][i] = imagePaths[i]
                        else:
                            st.session_state["chosenImagePaths"][i] = False
    ## Q&A tab
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

        with response_container:
            paint_history()
        with input_container:
            question = st.chat_input("여기에 물어보고 싶은 내용을 입력해주세요!")
        with response_container:
            if question:
                send_message(question, "human")
                with st.spinner("질문에 대한 답을 만들고 있습니다...."):
                    answer = get_first_answer(
                        question,
                        st.session_state["mainFilePath"],
                        openAI_API_KEY,
                    )

                    if isInclude_relatedFiles_toggle:
                        relatedFilePaths = []
                        for relatedFilePath in st.session_state[
                            "chosenRelatedFilePaths"
                        ]:
                            if relatedFilePath != False:
                                relatedFilePaths.append(relatedFilePath)
                        answer = get_document_refine_answer(
                            answer,
                            relatedFilePaths,
                            openAI_API_KEY,
                        )

                    if isInclude_images_toggle:
                        imagePaths = []
                        for imagePath in st.session_state["chosenImagePaths"]:
                            if imagePath != False:
                                imagePaths.append(imagePath)
                        answer = get_image_refine_answer(
                            answer,
                            imagePaths,
                            openAI_API_KEY,
                        )
                    send_message(answer, "ai")
    ## Q&A tab
    with quiz_tabs:
        if not st.session_state["start_status"]:
            st.write("퀴즈 페이지에 오신 걸 환영합니다.")
            difficulty = None
            make_quiz_button = None

            left, right = st.columns(2, vertical_alignment="bottom")

            with left:
                difficulty = st.selectbox(
                    "Choose quiz difficulty.", options=["Easy", "Hard"]
                )
            with right:
                make_quiz_button = st.button("퀴즈 만들기")

            if make_quiz_button:
                with st.spinner("퀴즈를 만들고 있습니다..."):
                    quiz_json = get_quiz_json(
                        st.session_state["mainFilePath"],
                        difficulty,
                        openAI_API_KEY,
                        st.session_state["quiz_change_value"],
                    )
                if quiz_json == "Error":
                    st.session_state["start_status"] = False
                else:
                    st.session_state["quiz_json"] = quiz_json
                    st.session_state["start_status"] = True
                    st.rerun()
        else:
            with st.sidebar:
                reset_button = st.button("Restart Quiz")
                if reset_button:
                    st.session_state["start_status"] = False
                    st.session_state["quiz_json"] = []
                    st.session_state["quiz_change_value"] = (
                        st.session_state["quiz_change_value"] + 1
                    )
                    st.rerun()

            with st.form("quiz_form"):
                correct_cnt = 0
                radio_key_value = 0
                questions = st.session_state["quiz_json"]
                radioList = []
                for question in questions:
                    st.write(question["question"])
                    value = st.radio(
                        "Select an answer",
                        [answer["answer"] for answer in question["answers"]],
                        index=None,
                        key=radio_key_value,
                    )
                    radio_key_value = radio_key_value + 1
                    if {"answer": value, "correct": True} in question["answers"]:
                        correct_cnt = correct_cnt + 1
                        st.success("Correct!")
                    elif value != None:
                        st.warning("Wrong")

                if correct_cnt == len(questions):
                    st.session_state["start_status"] = False
                    st.session_state["quiz_change_value"] = (
                        st.session_state["quiz_change_value"] + 1
                    )
                    st.balloons()
                    st.toast("You are perfect!", icon="🎉")
                    time.sleep(2)
                    st.rerun()

                st.form_submit_button("Submit")
