from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity


load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
documents =[
    "Shahid Afridi is pakistan all rounder cricketer. Also know as Lala",
    "Imran Khan, thee former pakistan cricketer, pakistan's prime minister and politician.Now in jail due to allegations of giving narratives against state",
    "Abdul Qadeer Khan, a scientist how invented atom bomb for Pakistan"
]
doc_embeddings = embeddings.embed_documents(documents)

query = "Who has three personalities, cricketer, prime minister and politician?"
query_embeddings = embeddings.embed_query(query)
sorted_embeddings = sorted(enumerate(cosine_similarity([query_embeddings], doc_embeddings)[0]), key=lambda x: x[1])
print(sorted_embeddings)
index, score = sorted_embeddings[-1]
print(query)
print(documents[index])
print("embedding socre", score)
