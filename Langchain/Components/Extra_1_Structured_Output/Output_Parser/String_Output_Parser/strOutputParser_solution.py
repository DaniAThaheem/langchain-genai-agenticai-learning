from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = HuggingFaceEndpoint(
    repo_id="",
    task="text-generation"
)
model = ChatHuggingFace(llm=llm)

chat_template1 = PromptTemplate(
    template=" Write a detailed note about the topic {topic}",
    input_variables=["topic"]
)

chat_template2 = PromptTemplate(
    template="Write a 5 lines summary of the topic {text}",
    input_variables=["text"]
)

parser = StrOutputParser()

chain = chat_template1 | model | parser | chat_template2 | model | parser

result = chain.invoke({"topic":"A student from village facing difficulties in modern era and how to compete witht the students of advanced city in the race of Technology."})

print(result)

