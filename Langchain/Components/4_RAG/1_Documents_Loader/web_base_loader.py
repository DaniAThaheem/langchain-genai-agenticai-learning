from langchain_community.document_loaders import WebBaseLoader


loader = WebBaseLoader(web_path="https://github.com/DaniAThaheem")

docs = loader.lazy_load()
for doc in docs:
    print(doc)