#Chat with LLM is stateless so we maintain the chat history
#While maintaining the chat history it is difficult to identify which message is form the human and which is from the AI

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

chat_history = []
while True:
    user_input = input("You: ")
    chat_history.append(user_input)
    if user_input == "exit":
        break
    result = model.invoke(chat_history)
    chat_history.append(result.content)
    print("AI: " + result.content)

print(chat_history)