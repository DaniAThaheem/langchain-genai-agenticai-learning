from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

messages = [
    SystemMessage(content="You are a corporate professional chatbot assistant")
]

while True:
    human_input = input("You: ")
    if human_input=="exit":
        break
    messages.append(HumanMessage(content=human_input))
    result = model.invoke(messages)
    messages.append(AIMessage(content=result.content))
    print(result.content)

print(messages)

