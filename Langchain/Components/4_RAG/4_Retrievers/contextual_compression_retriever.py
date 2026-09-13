from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

load_dotenv()

doc_1 = Document(
    page_content="""VLC media player is an open source media player famous for its ability to support Windows Operating System from a long time. It is a media player that beats a lot of media players in quality. It is famous and is like a convention followed by every Windows user. They follow this media player like a prescription to get rid of other paid media players David Warner is an Australian left-handed opening batter and the captain of Karachi Kings.He is known for his aggressive batting and ability to score quickly in T20 cricket.Warner brings extensive international and franchise cricket experience to Karachi Kings. His leadership and explosive opening batting make him one of the team's biggest attractions.""",
    metadata={"team": "Islamabad United", "player":'vlc'}
)

doc_3 = Document(
    page_content="""Shaheen Shah Afridi is a Pakistani left-arm fast bowler and the captain of Lahore Qalandars. He is particularly dangerous with the new ball and is known for generating pace and swing. Shaheen has played a major role in Lahore Qalandars' recent PSL success. His wicket-taking ability and leadership make him one of the most important players in the squad. MX player a media player famous for its ease of use and working especially for android. An old school media player setting its boundaries in the ground of new media players such a playit vlc for mobile and others.""",
    metadata={"team": "Lahore Qalandars", "player":"MX Player"}
)

docs = [doc_1, doc_3]


model = ChatGoogleGenerativeAI(model = "")

embedding_model = GoogleGenerativeAIEmbeddings(model= "")

compressor = LLMChainExtractor(model)

faiss_db = FAISS.from_documents(
    documents=docs,
    embedding=embedding_model
)

retriever = faiss_db.as_retriever(
    search_kwargs={"k":2}
)

contextual_retriever = ContextualCompressionRetriever(
    base_retriever=retriever,
    base_compressor=compressor
)

query = "Give info about VLC player"

docs = contextual_retriever.invoke(query)

for doc in docs:
    print(doc)


    


ContextualCompressionRetriever()