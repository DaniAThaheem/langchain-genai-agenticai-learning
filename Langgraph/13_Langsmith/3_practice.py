from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_classic.document_loaders import PyPDFLoader
import pathlib as Path
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

load_dotenv()

pdf_path = Path.Path(__file__).parent / "Project" / "Danish_Abbas_CV_SaudiPak_YEP_2026_v3.pdf"

pdf_loader = PyPDFLoader(str(pdf_path))
pdf_docs = pdf_loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
pdf_chunks = text_splitter.split_documents(pdf_docs)

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
vectorstore = FAISS.from_documents(pdf_chunks, embeddings)

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})
retriever_results = retriever.invoke("What is meant by supervised learning?")

prompt_template = PromptTemplate(
    
    input_variables=["context", "question"],
    template="You are a helpful assistant. Use the following context to answer the question.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
)

context = "\n".join([doc.page_content for doc in retriever_results])

prompt = prompt_template.invoke({
    "context": context,
    "question": "What are skills of danish?"
})

llm = ChatGoogleGenerativeAI(model = "gemini-flash-latest")

result = llm.invoke(prompt)

print(result)



