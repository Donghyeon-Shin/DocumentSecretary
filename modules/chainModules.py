import os
import json
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)
from langchain.schema.output_parser import StrOutputParser, BaseOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.callbacks import StdOutCallbackHandler
from langchain_community.vectorstores import FAISS


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
    streaming=True,
    callbacks=[StdOutCallbackHandler()],
)


class JsonOutputParser(BaseOutputParser):
    def parse(self, text):
        text = text.replace("```", "").replace("json", "")
        return json.loads(text)

format_function = {
    "name": "formatting_quiz",
    "description": "function that takes a list of questions and answers and returns a quiz",
    "parameters": {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                        },
                        "answers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "answer": {
                                        "type": "string",
                                    },
                                    "correct": {
                                        "type": "boolean",
                                    },
                                },
                                "required": ["answer", "correct"],
                            },
                        },
                    },
                    "required": ["question", "answers"],
                },
            }
        },
        "required": ["questions"],
    },
}


def format_doc(document):
    return "\n\n".join(doc.page_content for doc in document)


def embed_file(filePaths):
    # if not os.path.exists("./.cache/files"):
    #     os.makedirs("./.cache/files")
    if not os.path.exists("./.cache/embeddings"):
        os.makedirs("./.cache/embeddings")
    file_name = filePaths.split("/")[-1]
    loader = UnstructuredFileLoader(filePaths)
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=50,
    )
    cache_dir = LocalFileStore(f"./.cache/embeddings/{file_name}")
    docs = loader.load_and_split(text_splitter=splitter)
    embedder = OpenAIEmbeddings()
    cache_embedder = CacheBackedEmbeddings.from_bytes_store(embedder, cache_dir)
    vectorStore = FAISS.from_documents(docs, cache_embedder)
    return vectorStore.as_retriever()


def document_split(file_path, includeCode=True):
    loader = UnstructuredFileLoader(file_path=file_path)
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500,
        chunk_overlap=60,
    )
    docsList = loader.load()
    docs = docsList[0].page_content.split("\n\n")
    content = ""
    codeDocs = []
    codeDoc = ""
    flag = False
    for doc in docs:
        if "```" in doc:
            if flag:
                codeDocs.append(codeDoc)
                doc.replace("```", " ")
                flag = False
            else:
                codeDoc = ""
                flag = True

        if flag:
            codeDoc += doc + " "
        else:
            content += doc + " "
    textDocs = splitter.split_text(content)
    if includeCode:
        textDocs.extend(codeDocs)
    return textDocs


class Prompts:
    def get_main_refine_prompt(self):
        main_refine_prompt = ChatPromptTemplate.from_template(
            """
        Your job is to produce a final summary.
        You are very good at using Korean and English. but You must answer the question in Korean.
        We have provied an existing answer to a certain point : {existing_content}
        We have the opportunity to refine the existing answer (only if needed) with some more context below.
        ------
        {context}
        ------
        Given the new context, refine the original answer.
        If the context ins't useful, RETURN the original answer.
        DON'T make it up. 
        """
        )
        return main_refine_prompt

    def get_RAG_prompt(self):
        RAG_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                You are a helpful assistant. Answer questions using only the following context.
                DON'T make it up.
                --------
                {context}
                """,
                ),
                ("human", "{question}"),
            ]
        )
        return RAG_prompt

    def get_quiz_prompt(self):
        quiz_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a helpful assistant that is role playing as a teacher.
                    Based ONLY on the following context make 10 questions to test the user's knowledge about the text.
                    Each question should have 4 answer, three of them must be incorrect and one should be correct.
                    The problem is that there are two versions that are difficult and easy and they must be presented at the difficulty level desired by the user.
                    You should MAKE 10 Questoins
                    
                    Use (o) to signal the correct answer.

                    Question examples
                    
                    Question: What is the color of the occean?
                    Answers: Red|Yellow|Green|Blue(o)

                    Question: What is the capital or Georgia?
                    Answers: Baku|Tbilisi(o)|Manila|Beirut
                    
                    Question: When was Avator released?
                    Answers: 2007|2001|2009(o)|1998

                    Question: Who was Julius Caesar?
                    Answers: A Roman Emperor(o)|Painter|Actor|Model

                    Your turn!

                    Context: {context}
                    Difficulty : {difficulty}
                    """,
                )
            ]
        )
        return quiz_prompt


class Chains:
    prompts = Prompts()

    def run_Refine_chain(self, mainFilePath):
        if os.path.isfile(mainFilePath):
            mainDocs = document_split(mainFilePath)
        else:
            return "Error"

        main_refine_prompt = self.prompts.get_main_refine_prompt()

        main_refine_chain = main_refine_prompt | llm | StrOutputParser()

        answer = ""

        for doc in mainDocs:
            answer = main_refine_chain.invoke(
                {"existing_content": answer, "context": doc}
            )

        return answer

    def run_RAG_chain(self, mainFilePath, question):
        if os.path.isfile(mainFilePath):
            retriever = embed_file(mainFilePath)
        else:
            return "Error"

        main_RAG_prompt = self.prompts.get_RAG_prompt()
        main_RAG_chain = (
            {
                "context": retriever | RunnableLambda(format_doc),
                "question": RunnablePassthrough(),
            }
            | main_RAG_prompt
            | llm
            | StrOutputParser()
        )
        answer = main_RAG_chain.invoke(question)
        return answer

    def run_quiz_chain(self, fileContent, difficulty):
        llm = ChatOpenAI(
            temperature=0.1,
            model="gpt-3.5-turbo-0125",
        ).bind(
            function_call={
                "name": "formatting_quiz",
            },
            functions=[
                format_function,
            ],
        )

        quiz_prompt = self.prompts.get_quiz_prompt()
        quiz_chain = quiz_prompt | llm
        return quiz_chain.invoke({"context": fileContent, "difficulty": difficulty})
