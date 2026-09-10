from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel, RunnableSequence
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

parser = StrOutputParser()

template1 = PromptTemplate(
    template="Generate a tweet about {topic}",
    input_variables=["topic"]
)

template2 = PromptTemplate(
    template="Generate a linkedin post about {topic}",
    input_variables=["topic"]
)

chain = RunnableParallel(
    {
        "tweet": RunnableSequence(template1, model, parser),
        "linkedin": RunnableSequence(template2, model, parser)
    }
)

result = chain.invoke({"topic":"Mastering AI after Bachelors in Information Technology"})

print(result)