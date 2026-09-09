from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

prompt1 = PromptTemplate(
    template="Identify the main processes for getting {scholarship} for Masters in AI",
    input_variables=["scholarship"]
)

prompt2 = PromptTemplate(
    template="Write a brief report on the identified {points} and main points to increase the chances of getting the scholarship",
    input_variables=["points"]
)

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({"scholarship" : "Erasmus Mundis"})

print(result)
