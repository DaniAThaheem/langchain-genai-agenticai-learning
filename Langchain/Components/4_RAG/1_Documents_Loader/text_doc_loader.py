from pathlib import Path
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

template = PromptTemplate(
    template="Summarize the goal {goal}",
    input_variables=["goal"]
)

parser = StrOutputParser()

sample_path = Path(__file__).parent / "Sample" / "sample.txt"
document = Document(
    page_content= sample_path.read_text(encoding="utf-8"),
    meta_data = {"source" : sample_path}
)
docs = [document]
print(len(docs))
print(type(docs))
print(docs[0])
print(type(docs[0]))
content = docs[0]


chain = template | model | parser

print(chain.invoke({"goal": content}))




