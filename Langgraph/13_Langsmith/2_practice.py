from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm1 = ChatGoogleGenerativeAI(model="gemini-flash-latest")
llm2 = ChatGoogleGenerativeAI(model="gemini-flash-latest")

prompt1 = PromptTemplate(
    template="You are a professional writter about the Growth in Artifical Intelligence field. Write a long article meaningful about the topic {topic}.",
    input_variables=["topic"]
)
prompt2 = PromptTemplate(
    template="You are a professional writter who summarize the topic in a meaningful way about the Growth in Artifical Intelligence field. Write a summary about the article meaningful about the article {text}.",
    input_variables=["text"]
)

parser = StrOutputParser()

chain = prompt1 | llm1 | parser | prompt2 | llm2 | parser

result = chain.invoke({"topic":"Masters in Artifical Intelligence"})

print(result)