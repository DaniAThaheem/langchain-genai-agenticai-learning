from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langsmith import traceable
from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel, RunnableLambda
import pathlib as Path
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
path = Path.Path(__file__).parent / "Project" / "Danish_Abbas_CV_SaudiPak_YEP_2026_v3.pdf"
embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")

@traceable(name="doc_loader")
def doc_loader(path):
    loader = PyPDFLoader(str(path))
    docs = loader.load()
    return docs

@traceable(name="doc_splitter")
def doc_splitter(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    return chunks

@traceable(name="vector_store")
def vector_store(chunks):
    v_s = FAISS.from_documents(documents=chunks, embedding=embedding_model)
    return v_s

@traceable(name="setup_pipeline")
def setup_pipeline(path):
    docs = doc_loader(path)
    chunks = doc_splitter(docs)
    vs = vector_store(chunks)
    return vs


v_s = setup_pipeline(path)
retriever =v_s.as_retriever(search_type="similarity", search_kwargs={"k":3})

def format_data(extracted_docs):

    context = "\n".join([doc.page_content for doc in extracted_docs])
    return context

parallel_runnable = RunnableParallel({
    "context": itemgetter("question") | retriever | RunnableLambda(format_data),
    "question": itemgetter("question")
})


prompt = ChatPromptTemplate([
    ("system", "You are a professional writter, who explains everything from the given context and nothing from the outer concept"),
    ("human", "Here is the question {question} and the context related to the question is {context}")
]
    
)

parser = StrOutputParser()



chain = parallel_runnable | prompt | llm | parser

result = chain.invoke({"question": "What are the contact details of danish abbas?"})

print(result)




