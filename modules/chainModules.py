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

    def get_questions_prompt(self):
        questions_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a helpful assistant that is role playing as a teacher.
                    Based ONLY on the following context make 10 questoins to test the user's knowledge about the text.
                    Each question should have 4 answers, three of them must be incorrect and one should be correct.
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
                    """,
                )
            ]
        )
        return questions_prompt

    def get_formatting_prompt(self):
        formatting_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a powerful formatting algorithm.
                    You format exam question into JSON format.
                    
                    Answers with (o) are the correct ones.

                    Example Input:

                    Question: What is the color of the occean?
                    Answers: Red|Yellow|Green|Blue(o)
                    
                    Question: What is the capital or Georgia?
                    Answers: Baku|Tbilisi(o)|Manila|Beirut

                    Question: When was Avator released?
                    Answers: 2007|2001|2009(o)|1998

                    Question: Who was Julius Caesar?
                    Answers: A Roman Emperor(o)|Painter|Actor|Model

                    Example Output:
                    ```json
                    {{ "questions": [
                            {{
                                "question": "What is the color of the occean?",
                                "answers": [
                                    {{
                                        "answer": "Red",
                                        "correct": false
                                    }},
                                    {{
                                        "answer": "Yellow"
                                        "correct": false
                                    }},
                                    {{
                                        "answer": "Green",
                                        "correct": false
                                    }},
                                    {{
                                        "answer": "Blue",
                                        "correct": true
                                    }},
                                ]
                            }},
                            {{
                                "question": "What is the capital or Georgia?",
                                "answers": [
                                    {{
                                        "answer": "Baku",
                                        "correct": false
                                    }},
                                    {{
                                        "answer": "Tbilisi"
                                        "correct": true
                                    }},
                                    {{
                                        "answer": "Manila",
                                        "correct": false
                                    }},
                                    {{
                                        "answer": "Beirut",
                                        "correct": false
                                    }},
                                ]
                            }},
                            {{
                                "question": "When was Avator released?",
                                "answers": [
                                    {{
                                        "answer": "2007",
                                        "correct": false
                                    }},
                                    {{
                                        "answer": "2001"
                                        "correct": false
                                    }},
                                    {{
                                        "answer": "2009",
                                        "correct": true
                                    }},
                                    {{
                                        "answer": "1998",
                                        "correct": false
                                    }},
                                ]
                            }},
                            {{
                                "question": "Who was Julius Caesar?",
                                "answers": [
                                    {{
                                        "answer": "A Roman Emperor",
                                        "correct": true
                                    }},
                                    {{
                                        "answer": "Painter"
                                        "correct": false
                                    }},
                                    {{
                                        "answer": "Actor",
                                        "correct": false
                                    }},
                                    {{
                                        "answer": "Model",
                                        "correct": false
                                    }},
                                ]
                            }}                                                
                        ]
                    }}```

                    Your turn!

                    Question : {context}
                    """,
                )
            ]
        )
        return formatting_prompt


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

    def run_quiz_chain(self, filePath):
        doc = ""
        if os.path.isfile(filePath):
            with open(filePath, "r", encoding="UTF-8") as f:
                doc = f.read()
        else:
            return "Error"

        questions_prompt = self.prompts.get_questions_prompt()
        formatting_prompt = self.prompts.get_formatting_prompt()
        output_parser = JsonOutputParser()
        questions_chain = questions_prompt | llm
        formatting_chain = formatting_prompt | llm
        chain = {"context": questions_chain} | formatting_chain | output_parser
        return chain.invoke(doc)
