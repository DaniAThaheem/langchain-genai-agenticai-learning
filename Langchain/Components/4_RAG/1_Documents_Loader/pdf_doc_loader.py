from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path


load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

template = PromptTemplate(
    template="Give the feed back about {topic1} and {topic2}",
    input_variables=["topic1", "topic2"]
)

parser = StrOutputParser()

pdf_path = Path(__file__).parent / "Sample" / "Danish_Abbas_CV_Getz_Pharma.pdf"

pdf_loader = PyPDFLoader(file_path=pdf_path)

docs = pdf_loader.load()

print(len(docs))

topic1 = docs[0].page_content
topic2 = docs[1].page_content

chain = template | model | parser

print(chain.invoke({"topic1": topic1, "topic2": topic2}))








