from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

chat_template = ChatPromptTemplate([
    ("system", "You are a {domain} expert. A top level expert which knows, explain and provide solution in depth"),
    ("human", "The topic which requires a deep explanatin is {topic}")
    
])
domain = input("Enter domain: ")
topic = input("Enter topic: ")

prompt = chat_template.invoke({
 "domain": domain,
 "topic": topic
})

result = model.invoke(prompt)
print(result.content)