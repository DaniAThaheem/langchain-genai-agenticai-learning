from langchain_community.retrievers import WikipediaRetriever


retriever = WikipediaRetriever(
    top_k_results= 2,
    lang='en'
) 

query = "What is the geopolitical history of Pakistan and India from the chinese perspective?"

docs = retriever.invoke(query)

for doc in docs:
    print(doc.page_content)

