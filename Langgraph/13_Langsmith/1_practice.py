from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")

prompt = PromptTemplate(
    template="You are a professional tech journalist. Answer the question {question}. Don\'t bise no matter what topic it is asked in the question.",
    input_variables=["question"]
)

parser = StrOutputParser()

chain = prompt | llm | parser
result = chain.invoke({"question":"What is the future of AI in terms of replacing the human"})

print(result)