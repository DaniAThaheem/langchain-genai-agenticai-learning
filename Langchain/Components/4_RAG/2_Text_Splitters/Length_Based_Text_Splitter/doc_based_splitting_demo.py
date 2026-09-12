from langchain_text_splitters import CharacterTextSplitter
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

pdf_path = Path(__file__).parent / "Sample" / "Danish_Abbas_CV_Getz_Pharma.pdf"
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

spliter = CharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=5,
    separator=""
)

print(docs[0])

chunks = spliter.split_documents(docs)

#List of chunks of documents
print(chunks)