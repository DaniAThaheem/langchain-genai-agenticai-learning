from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from pathlib import Path


directory_path = Path(__file__).parent / "Sample" / "Sample_Files"

loader = DirectoryLoader(
    path = directory_path,
    glob="*.pdf",
    loader_cls=PyPDFLoader
)


#First Load Everything and Then Show

# docs = loader.load()

# for doc in docs:
#     print(doc.metadata)



#Load on Demand and show at the same time

docs = loader.lazy_load()

for doc in docs:
    print(doc.metadata)