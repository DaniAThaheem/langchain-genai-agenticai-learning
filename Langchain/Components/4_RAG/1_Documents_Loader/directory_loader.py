from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

template =PromptTemplate(
    template="Executive summary of the page and score it out of 10 according to ATS and the page content is {page}",
    input_variables=["page"]
)

parser = StrOutputParser()

directory_path = Path(__file__).parent / "Sample" / "Sample_Files"

loader = DirectoryLoader(
    path = directory_path,
    glob="*.pdf",
    loader_cls=PyPDFLoader
)

docs = loader.load()

print(len(docs))
print(docs[0].page_content)
print(docs[0].metadata)

doc1 = docs[0].page_content

chain = template | model | parser

print(chain.invoke({"page":doc1}))

