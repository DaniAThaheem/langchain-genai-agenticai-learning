from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")
result = model.invoke("What is the current condition of Pakistan Cricket Team? Give a deep analysis")
print(result)
print(result.content)