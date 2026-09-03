from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
documents = [
    "Google AI in image generation",
    "Google AI in text generation",
    "Google AI in video generation"
]
result = model.embed_documents(documents)
print(result)