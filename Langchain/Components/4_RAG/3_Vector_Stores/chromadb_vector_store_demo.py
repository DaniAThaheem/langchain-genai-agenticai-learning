from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

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

doc_4 = Document(
    page_content="""Babar Azam is a Pakistani right-handed batter and a key player for Peshawar Zalmi. He is regarded as one of Pakistan's leading modern-era batters and is known for his technically strong stroke play. Babar was the leading run-scorer of PSL 2026 with 588 runs. His consistency and ability to build innings make him a central figure in Peshawar Zalmi's batting lineup.""",
    metadata={"team": "Peshawar Zalmi"}
)

doc_5 = Document(
    page_content="""Saud Shakeel is a Pakistani left-handed batter and the captain of Quetta Gladiators. He is known for his technically sound batting and ability to build partnerships. Saud also contributes with his slow left-arm orthodox bowling when required. His batting ability and leadership make him an important part of Quetta Gladiators.""",
    metadata={"team": "Quetta Gladiators"}
)

doc_6 = Document(
    page_content="""Marnus Labuschagne is an Australian right-handed batter who played for Hyderabad Kingsmen in PSL 2026. He was the team's major international signing and brought significant experience from Australian cricket. Labuschagne scored 360 runs in 13 innings during PSL 2026 at a strike rate of 134. His batting experience and leadership made him one of the standout players for the new franchise.""",
    metadata={"team": "Hyderabad Kingsmen"}
)

doc_7 = Document(
    page_content="""Mohammad Rizwan is a Pakistani wicketkeeper-batter and the captain of Rawalpindiz. He is a right-handed batter known for consistency, fitness, and strong wicketkeeping skills. Rizwan has been one of Pakistan's most successful T20 batters and has extensive PSL experience. His leadership, batting reliability, and wicketkeeping make him a crucial player for Rawalpindiz.""",
    metadata={"team": "Rawalpindiz"}
)

doc_8 = Document(
    page_content="""Steven Smith is an Australian right-handed batter who played for Multan Sultans in PSL 2026. He is an experienced international cricketer known for his unusual but highly effective batting technique. Smith brings extensive experience from international and franchise cricket to the Multan Sultans squad. His experience and ability to anchor an innings make him a valuable player for the team.""",
    metadata={"team": "Multan Sultans"}
)

chromadb = Chroma(
            embedding_function=GoogleGenerativeAIEmbeddings(model="gemini-embedding-2"),
            persist_directory= "chroma_db",
            collection_name="sample"
        )

docs  = [doc_1, doc_2, doc_3, doc_4, doc_5, doc_6, doc_7, doc_8]
while True:
    print("""
    1. Convert documents into embeddings
    2. Read Data from the Data base
    3. Ask question
    4. Ask question and get score with ranking (less score more accuracy)
    5. Update the document
    6. Delete the document
    7. Exit the program
    """)

    x = int(input("Enter the use case number: "))

    match x:
        case 1:
            ids = chromadb.add_documents(docs)
            print(ids)
        case 2:
            info_dict =chromadb.get(include=["ids", "documents", "embeddings", "metadata"])
            print(info_dict)
            
        case 3:
            query = input("Write the query: ")
            players = chromadb.similarity_search(query=query, k = 8)
            for player in  players:
                print(player)

        case 4:
            query = input("Write the query: ")
            players = chromadb.similarity_search_with_score(query=query, k = 8)
            for player in  players:
                print("Here is the palyer and its score: ")
                print(player)

        case 5:
            id_to_update = input("Write id to update: ")
            doc_to_replace = Document(
                page_content="""Mohammad Rizwan is a Pakistani wicketkeeper-batter and the captain of Rawalpindiz. He is a right-handed batter known for consistency, fitness, and strong wicketkeeping skills. Rizwan has been one of Pakistan's most successful T20 batters and has extensive PSL experience. His leadership, batting reliability, and wicketkeeping make him a crucial player for Rawalpindiz""",
                metadata={"team": "Rawalpindiz"}
            )
            chromadb.update_document(document_id=id_to_update, document=doc_to_replace)

        case 6:
            id_to_delete = input("Enter id to delete that document")
            chromadb.delete(ids=[id_to_delete])
            remaining_data=chromadb.get(["ids", "documents", "embeddings", "metadata"])
            print(remaining_data)

        case 7:
            break

