from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel, RunnableSequence, RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

parser = StrOutputParser()

template1 = PromptTemplate(
    template="Generate a joke about {topic}",
    input_variables=["topic"]
)

template2 = PromptTemplate(
    template="Generate explanation about this joke {joke}",
    input_variables=["joke"]
)

sequence_chain = RunnableSequence(template1, model, parser)

parallel_chain = RunnableParallel(
    {
        "explanation": RunnableSequence(template2, model, parser),
        "joke": RunnablePassthrough()
    }
)

final_chain = RunnableSequence(sequence_chain, parallel_chain)

result = final_chain.invoke({"topic":"AI in Video Generation"})

print(result)

