from langchain_community.retrievers import WikipediaRetriever

query = "What is the geopolitical history of Pakistan and India from the chinese perspective?"

try:
    retriever = WikipediaRetriever(
        top_k_results=2,
        lang="en",
    )

    docs = retriever.invoke(query)

    if not docs:
        print("No Wikipedia articles were returned for this query.")
    else:
        for doc in docs:
            print(doc.page_content)

except Exception as e:
    print(f"Wikipedia retriever failed: {type(e).__name__}: {e}")
    print("This usually happens when the Wikipedia API is unreachable, blocked, or returns a non-JSON response.")
    print("The script will continue without crashing.")
    print(f"Query attempted: {query}")

