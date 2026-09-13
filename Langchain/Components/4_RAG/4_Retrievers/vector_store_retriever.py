from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

model = GoogleGenerativeAIEmbeddings(model="")

doc_1 = Document(
    page_content="""Shadab Khan is a Pakistani all-rounder and the captain of Islamabad United. He is a right-handed batter and right-arm leg-spin bowler known for his attacking style. Shadab has been one of the important players in Islamabad United's PSL campaigns. His leadership, batting, and leg-spin bowling make him a key player for the team.""",
    metadata={"team": "Islamabad United"}
)

doc_2 = Document(
    page_content="""David Warner is an Australian left-handed opening batter and the captain of Karachi Kings.He is known for his aggressive batting and ability to score quickly in T20 cricket.Warner brings extensive international and franchise cricket experience to Karachi Kings. His leadership and explosive opening batting make him one of the team's biggest attractions.""",
    metadata={"team": "Karachi Kings"}
)

doc_3 = Document(
    page_content="""Shaheen Shah Afridi is a Pakistani left-arm fast bowler and the captain of Lahore Qalandars. He is particularly dangerous with the new ball and is known for generating pace and swing. Shaheen has played a major role in Lahore Qalandars' recent PSL success. His wicket-taking ability and leadership make him one of the most important players in the squad.""",
    metadata={"team": "Lahore Qalandars"}
)

docs = [doc_1, doc_2, doc_3]

chromadb_instance = Chroma.from_documents(
    documents=docs,
    embedding=model,
    collection_name='sample_2'
)


retriever = chromadb_instance.as_retriever(
    search_type="similarity",
    search_kwargs={"k":1}
)

query = "Which player plays for Karachi Kings?"

docs = retriever.invoke(query)

for doc in docs:
    print(doc.page_content)

