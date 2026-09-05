from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

chat_template = ChatPromptTemplate([
    ("system", "You are a pro master chatbot assistant"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{query}")
])

chat_history =[]

with open("chat_history.txt") as f:
    chat_history.extend(f.readlines)

prompt = chat_template.invoke({
    "chat_history":chat_history,
    "query":"I want my refund right now. It is 24th hour after my request and still I could not get it"
})

print(prompt)

result = model.invoke(prompt)

print(result)