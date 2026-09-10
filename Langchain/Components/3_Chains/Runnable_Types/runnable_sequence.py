from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

template = PromptTemplate(
    template="Predict the future about the give technology {technology}",
    input_variables=["technology"]
)

parser = StrOutputParser()

chain = RunnableSequence(template, model, parser)

result = chain.invoke({"technology": "AI"})

print(result)