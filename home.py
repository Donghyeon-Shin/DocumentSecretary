import os
import streamlit as st
import zipfile
from modules.crewModules import Crews

st.set_page_config(
    page_title="Document Secretary",
    page_icon="🖥️",
)

st.title("Document Secretary")

st.markdown(
    """
    환영합니다👍\n
    당신이 정리한 문서를 바탕으로 질문에 답을 하고 원하시면 문제도 만들어드릴게요!\n
    'Side Bar'에 정리한 문서들을 ZIP 형태로 넣어주세요.\n
    """
)

if "isSuccessFile" not in st.session_state:
    st.session_state["isSuccessFile"] = False

if "isLoadFile" not in st.session_state:
    st.session_state["isLoadFile"] = False

if "filePaths" not in st.session_state:
    st.session_state["filePaths"] = {}

with st.sidebar:
    file = st.file_uploader("문서 경로를 지정해주세요.", type="zip")

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
    else:
        st.session_state["isSuccessFile"] = False
        st.session_state["isLoadFile"] = False
        st.session_state["filePaths"] = {}

if st.session_state["isSuccessFile"]:
    crews = Crews()
    loadFile_tabs, summary_tabs, quiz_tabs = st.tabs(
        ["파일 불러오기", "질문하기", "문제 만들기"]
    )

    with loadFile_tabs:
        if st.session_state["isLoadFile"]:
            st.error("이미 파일을 로드하였어요!!")

        with st.form("file_option_form"):
            extension_name = st.selectbox(
                "읽을 파일들의 확장자를 선택해주세요.",
                (".pdf", ".txt", ".md", ".docx"),
            )
            keyward = st.text_input("찾고 싶은 키워드를 입력해주세요.", placeholder="단어로 입력할수록 더 정확하게 찾을 수 있어요!")

            doc_search_button = st.form_submit_button(
                "관련 문서 검색(비용이 발생하니 조심하세요!!)"
            )

            if doc_search_button:
                with st.status("파일을 불러오기...", expanded=True) as status:
                    st.write("지정된 경로에 있는 모든 파일을 불러오고 있습니다...")
                    docPathCrewResult = crews.run_docPathSearch(
                        extension_name=extension_name, file_path="./file"
                    )

                    if docPathCrewResult == "Error":
                        status.update(
                            label="파일을 불러오는데 오류가 발생했습니다.",
                            expanded=False,
                            state="error",
                        )
                    else:
                        st.write(
                            "불러온 파일 중 키워드에 맞는 파일들을 찾고 있습니다..."
                        )
                        docPaths = []
                        for docPath in docPathCrewResult["filePaths"]:
                            if os.path.splitext(docPath)[1] == extension_name:
                                docPaths.append(docPath)

                        fileSelectCrewResult = crews.run_fileSelect(keyward, docPaths)

                        if fileSelectCrewResult == "Error":
                            status.update(
                                label="파일을 불러오는데 오류가 발생했습니다.",
                                expanded=False,
                                state="error",
                            )
                        else:
                            st.session_state["isLoadFile"] = True
                            status.update(label="파일을 불러왔습니다.", expanded=False)
                            st.session_state["filePaths"] = fileSelectCrewResult

        if st.session_state["filePaths"] != {}:
            st.session_state["filePaths"]
