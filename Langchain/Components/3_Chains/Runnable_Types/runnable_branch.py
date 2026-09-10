from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.runnables import RunnableBranch, RunnableSequence, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

model = ChatGoogleGenerativeAI("gemini-flash-latest")

parser = StrOutputParser()

template1 = PromptTemplate(
    template="Write a detailed report about {topic}",
    input_variables=["topic"]
)

template2 = PromptTemplate(
    template="Executive summary of {text}",
    input_variables=["text"]
)

sequnence_chain = RunnableSequence(template1, model, parser)
parallel_chain = RunnableBranch(
    (lambda x: x.split() > 50, RunnableSequence(template2, model, parser)),
    RunnablePassthrough()
)

final_chain = RunnableSequence(sequnence_chain, parallel_chain)

result = final_chain.invoke({"topic":"Masters in AI according to current era"})

print(result)

