from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.8-flash")
result = model.invoke("What is the current condition of Pakistan Cricket Team? Give a deep analysis", temperature=0.3)
print(result)
print(result.content)