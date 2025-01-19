import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import BaseOutputParser


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
            },
        },
        "required": ["questions"],
    },
}


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

    def run_quiz_chain(self, fileContent, difficulty, openAI_API_KEY):
        llm = ChatOpenAI(
            temperature=0.1,
            model="gpt-4o-mini",
            api_key=openAI_API_KEY,
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
