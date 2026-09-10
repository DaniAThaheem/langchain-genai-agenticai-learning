from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

parser = StrOutputParser()

template1 = PromptTemplate(
    template="Generate a joke about {topic}",
    input_variables=["topic"]
)

template2 = PromptTemplate(
    template="Generate an explanation about the joke - {text}",
    input_variables=["text"]
)

sequence_chain = RunnableSequence(template1, model, parser)
parallel_chain = RunnableParallel(
    {
        "joke": RunnableSequence(template2, model, parser),
        "count":RunnableLambda(lambda x: len(x.split()))
    }
)

chain = RunnableSequence(sequence_chain, parallel_chain)

result = chain.invoke({"topic":"AI in sports"})

print("""{} \n Count: {}""".format(result["joke"], result["count"]))