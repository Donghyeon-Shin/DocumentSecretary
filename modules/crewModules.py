import os
import json
from crewai import LLM, Agent, Task, Crew
from crewai_tools import FileReadTool, DirectoryReadTool, VisionTool
from pydantic import BaseModel
from typing import List


class filePath(BaseModel):
    filePaths: List[str]


class mainFileContent(BaseModel):
    mainFile: str


class associateFilePath(BaseModel):
    relatedFiles: List[str]
    imageFiles: List[str]


class Agents:

    def __init__(self, openAI_API_KEY):
        self.gpt_4o_mini = LLM(
            model="gpt-4o-mini",
            temperature=0.1,
            api_key=openAI_API_KEY,
        )

        self.gpt_3_5 = LLM(
            model="gpt-3.5-turbo-1106",
            temperature=0.1,
            api_key=openAI_API_KEY,
        )

    def docPathSearcher(self):
        return Agent(
            role="docPathSearcher",
            goal="Finds the Filename extension : {extension_name} files inside {file_path} path. Should never modify the path of the file.",
            backstory="You are very good at finding markdown files.",
            allow_delegation=False,
            verbose=True,
            llm=self.gpt_4o_mini,
            tools=[
                DirectoryReadTool(),
            ],
        )

    def imgPathSearcher(self):
        return Agent(
            role="imgPathSearcher",
            goal="Finds the img files inside {img_path} path",
            backstory="You are fluent in Korean, and you are very good at finding image files.",
            allow_delegation=False,
            verbose=True,
            llm=self.gpt_3_5,
            tools=[
                DirectoryReadTool(),
            ],
        )

    def mainFileSearcher(self):
        return Agent(
            role="mainFileSearcher",
            goal="""
            Print out ONLY one document path that can answer {question}.
            if filepath does not appear to be related to the question.
            """,
            backstory="You are fluent in Korean. You have a talent for finding files that seem to solve questions.",
            allow_delegation=False,
            verbose=True,
            llm=self.gpt_3_5,
        )

    def fileReader(self):
        return Agent(
            role="fileReader",
            goal="""
            Print out ONLY one document. To use the Tool, The parameter MUST be file_path = `filepath`. 
            It should be outputted as it is without modification.
            """,
            backstory="You are fluent in Korean. You are a bookworm.",
            allow_delegation=False,
            verbose=True,
            llm=self.gpt_3_5,
            tools=[
                FileReadTool(),
            ],
        )

    def fileSelector(self):
        return Agent(
            role="fileSelector",
            goal="Find out the path of all other files that correspond to the document and print them out.",
            backstory="You are a file search expert and fluent in Korean. You have a great ability to read and analyze the details of the file.",
            llm=self.gpt_4o_mini,
            allow_delegation=False,
            verbose=True,
        )

    def questionRespondent(self):
        return Agent(
            role="questionRespondent",
            goal="Answer the question in a state based on specific content.",
            backstory="You are a great teacher. You're ready to answer any questions. You are also very good at using Korean and English.",
            llm=self.gpt_3_5,
            allow_delegation=False,
            verbose=True,
        )

    def refineRespondent(self):
        return Agent(
            role="refineRespondent",
            goal="Use the contents of the document to further specify the answer.",
            backstory="You are fluent in Korean, and You want the answer to be structured to make it easier for users to understand.",
            allow_delegation=False,
            verbose=True,
            llm=self.gpt_3_5,
        )

    def imgExtracter(self):
        return Agent(
            role="imgExtracter",
            goal="Extract the image files. and Add supplementary content to understand the contents of the existing answer. To use the Tool, The parameter MUST be image_path = `image_path`.",
            backstory="You are fluent in Korean, and You have a good ability to read images and convert them into text.",
            allow_delegation=False,
            verbose=True,
            llm=self.gpt_3_5,
            tools=[
                VisionTool(),
            ],
        )

    def documentSummarizer(self):
        return Agent(
            role="documentSummarizer",
            goal="Give the document and explain it in detail to make it easier to understand.",
            backstory="You are fluent in Korean, and You have a tremendous ability to understand and summarize the contents of the document.",
            allow_delegation=False,
            verbose=True,
            llm=self.gpt_3_5,
        )


class Tasks:
    def docPathSearch(self, agent):
        return Task(
            description="""
            Finds ALL the files and inside Directory
            File name extension : {extension_name}
            Directory path : {file_path}
            """,
            expected_output="Your final answer MUST be {extension_name} file path. NEVER arbitrarily modify the path. Just Answer path in file_path. Never include files from other extensions.",
            agent=agent,
            output_json=filePath,
            output_file="docPath.md",
        )

    def imgPathSearch(self, agent):
        return Task(
            description="Finds ALL the image files and inside {img_path} path.",
            expected_output="Your final answer MUST be image path. NEVER arbitrarily modify the path. Just Answer path in file_path",
            agent=agent,
            output_json=filePath,
            output_file="ImgPath.md",
        )

    def mainFileSearch(self, agent):
        return Task(
            description="""
            You have a file path list. Search Only one file path that can solve question.
            NEVER modify the file path in fileSelect.
            
            file_path : {docPaths}
            question : {question}
            """,
            expected_output="""
            Print out the path of the file you read.

            if filepath does not appear to be related to the question,
            DON'T read ANY Files. JUST Answer 'No files are associated.'
            """,
            agent=agent,
            output_json=mainFileContent,
            output_file="mainFilePath.md",
        )

    def fileRead(self, agent):
        return Task(
            description="""
            Read the file in the given path and output it as it is WITHOUT modification.
            
            Read the entire contents of the file based on the file path and print it out.
            DON'T do this more than once.

            file_path : {file_path}
            """,
            expected_output="""
            Never modify it and print out the file you read as it is.
            """,
            agent=agent,
            output_file="mainFileRead.md",
        )

    def fileSelect(self, agent, context):
        return Task(
            description="""
            Based on the fileRead, 
            There are other documents linked by the symbol '[[...]]' and '![[...]]' in that file NOT '[...]
            '[[...]]' symbol means a markdown file and '![[...]]' means an image file.
            
            Find all of the '[[...]]' and '![[...]]' and print out the ONLY file path associated with the word in it in file path list. 
            All file paths should EXIST in that markdownPathSearch Output or imgPathSearch Output. 
            DON'T make it up and look for it.
            If the relevant document/image does not exist, JUST Return EMPTY List.",

            relatedFiles List : {docPaths}
            ---------------------------------
            imageFiles List : {imgPaths}
            """,
            expected_output="""
            Your final answer MUST include the path of other related files and images within that file.
            You must select paths within EACH LIST.
            It doesn't include ANYTHING other than file paths. 
            NEVER modify the path of the file.

            Example Answer 1
            {
                "relatedFiles": [
                    "./Algorithm/Algorithm Content/Graph Theory/DFS(Depth-First Search).md",
                    "./Algorithm/Algorithm Content/Graph Theory/BFS(Breadth-First Search).md",
                    "./Algorithm/Algorithm Content/Tree/Union Find.md",
                ],
                "imageFiles": ["./Algorithm/Reference/Tree Reference/MST Ref/MST Graph.png",]
            }

            Example Answer 2
            {
                "relatedFiles": [],
                "imageFiles": [
                    "./Algorithm/Reference/Graph Theory Reference/BASE TREE.png",
                    "./Algorithm/Reference/Graph Theory Reference/BFS Ref/BFS Queue.png",
                ]
            }

            Example Answer 3
            {
                "relatedFiles": [
                    "./c/g.md",
                    "./c/c.md",
                    "./c/d.md",
                ],
                "imageFiles": []
            }        
            """,
            agent=agent,
            context=context,
            output_json=associateFilePath,
            output_file="associateFilePath.md",
        )

    def questionRespond(self, agent):
        return Task(
            description="""
            Read content and Find the correct answer to the question.
            
            It's the question you'll answer.
            question : {question}

            And below is the contents of the document you should refer to.
            ------
            {content}
            ------
            """,
            expected_output="""
            You should answer the question in as much detail as you can.
            You must answer in Korean.
            If the question doesn't include that content, Just Say 'I Don't know'.
            """,
            agent=agent,
            output_file="questionRespond.md",
        )

    def refineRespond(self, agent):
        return Task(
            description="""
            Read file content and Add supplementary content to understand the contents of the existing answer.
            We have provied an existing answer to a certain point : {existing_content}
            We have the opportunity to refine the existing answer (only if needed) with some more context below.
            ------
            {file_content}
            ------
            """,
            expected_output="""
            Given the new context, refine the original answer.
            If the context ins't useful, RETURN the original answer.
            You must answer in Korean.
            """,
            agent=agent,
            output_file="questionRefineContent.md",
        )

    def imgExtract(self, agent):
        return Task(
            description="""
            Read all the img files and Add supplementary content to understand the contents of the existing answer.
            NEVER modify the file path.
            You are very good at using Korean and English.
            We have provied an existing answer to a certain point : {existing_content}
            We have the opportunity to refine the existing answer (only if needed) with some more context below.
            ------
            {img_path}
            ------
            """,
            expected_output="""
            Given the new context, refine the original answer.
            If the context ins't useful, RETURN the original answer.
            You must answer in Korean.
            """,
            agent=agent,
            output_file="ImgExtractContent.md",
        )

    def documentSummerize(self, agent):
        return Task(
            description="""
            Read content and Summerize the contents in detail.
            
            Below is the contents of the document you should refer to.
            ------
            {content}
            ------
            """,
            expected_output="""
            You should answer document in as much detail as you can.
            You must answer in Korean.
            If the question doesn't include that content, Just Say 'I Don't know'.
            """,
            agent=agent,
            output_file="documentSummary.md",
        )


class Crews:
    def __init__(self, openAI_API_KEY):
        self.agents = Agents(openAI_API_KEY)
        self.tasks = Tasks()

    def run_docPathSearch(self, extension_name, file_path):
        docPathSearcher = self.agents.docPathSearcher()
        docPathSearcher_task = self.tasks.docPathSearch(docPathSearcher)

        filePathCrew = Crew(
            agents=[docPathSearcher],
            tasks=[docPathSearcher_task],
            verbose=True,
        )

        filePathResult = filePathCrew.kickoff(
            dict(
                extension_name=extension_name,
                file_path=file_path,
            )
        )

    def run_imgPathSearch(self, img_path):
        imgPathSearcher = self.agents.imgPathSearcher()
        imgPathSearcher_task = self.tasks.imgPathSearch(imgPathSearcher)

        filePathCrew = Crew(
            agents=[imgPathSearcher],
            tasks=[imgPathSearcher_task],
            verbose=True,
        )

        filePathResult = filePathCrew.kickoff(
            dict(
                img_path=img_path,
            )
        )

    def run_mainFileSearcher(self, docPathsStr: str, keyward):
        mainFileSearcher = self.agents.mainFileSearcher()
        mainFileSearcher_task = self.tasks.mainFileSearch(mainFileSearcher)

        mainFileSelectorCrew = Crew(
            agents=[
                mainFileSearcher,
            ],
            tasks=[
                mainFileSearcher_task,
            ],
            verbose=True,
        )

        mainFileSelectorResult = mainFileSelectorCrew.kickoff(
            dict(
                docPaths=docPathsStr,
                question=keyward,
            )
        )

    def run_fileSelect(self, keyward, mainFilePath, docPathsStr, imgPathsStr):
        fileReader = self.agents.fileReader()
        fileSelector = self.agents.fileSelector()

        fileReader_task = self.tasks.fileRead(fileReader)
        fileSelector_task = self.tasks.fileSelect(
            fileSelector,
            [fileReader_task],
        )

        fileSelectorCrew = Crew(
            agents=[
                fileReader,
                fileSelector,
            ],
            tasks=[
                fileReader_task,
                fileSelector_task,
            ],
            verbose=True,
        )

        fileSelectorResult = fileSelectorCrew.kickoff(
            dict(file_path=mainFilePath, docPaths=docPathsStr, imgPaths=imgPathsStr)
        )

    def run_questionRespondent(self, question, fileContent):
        questionRespondent = self.agents.questionRespondent()
        questionRespondent_task = self.tasks.questionRespond(questionRespondent)

        questionRespondentCrew = Crew(
            agents=[
                questionRespondent,
            ],
            tasks=[
                questionRespondent_task,
            ],
            verbose=True,
        )

        result = questionRespondentCrew.kickoff(
            dict(question=question, content=fileContent)
        ).raw
        return result

    def run_document_refine_crew(self, existing_content, relatedFileContentList):

        refineRespondent = self.agents.refineRespondent()
        refineRespondent_task = self.tasks.refineRespond(refineRespondent)

        questionRespondentCrew = Crew(
            agents=[
                refineRespondent,
            ],
            tasks=[
                refineRespondent_task,
            ],
            verbose=True,
        )

        for relatedFileContent in relatedFileContentList:
            existing_content = questionRespondentCrew.kickoff(
                dict(existing_content=existing_content, file_content=relatedFileContent)
            ).raw

        return existing_content

    def run_image_refine_crew(self, content, imgFilePaths):

        imgExtracter = self.agents.imgExtracter()
        imgExtracter_task = self.tasks.imgExtract(imgExtracter)

        imgExtracterCrew = Crew(
            agents=[
                imgExtracter,
            ],
            tasks=[
                imgExtracter_task,
            ],
            verbose=True,
        )

        content = imgExtracterCrew.kickoff(
            dict(existing_content=content, img_path=imgFilePaths)
        ).raw

        return content

    def run_document_summary_crew(self, fileContent):
        documentSummarizer = self.agents.documentSummarizer()
        documentSummarizer_task = self.tasks.documentSummerize(documentSummarizer)

        documentSummarizerCrew = Crew(
            agents=[
                documentSummarizer,
            ],
            tasks=[
                documentSummarizer_task,
            ],
            verbose=True,
        )

        content = documentSummarizerCrew.kickoff(dict(content=fileContent)).raw
        return content
