from langchain_experimental.text_splitter import SemanticChunker
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

text = """
Erasmus Mundis scholarship is a prestigiuos scholarship to study in Europe.Imran Khan was arrested in the past due to the allgations of anti-state actions.India, a country in the east of Pakistan is trying to spread fear of terrorism in Pakistan by using the betrayed people of Balochistan.
My name is danish and i am living in a village and my village is very beautiful. It exists near the Motorway N-5. We do farming for living. My father works in factory.
"""


splitter = SemanticChunker(GoogleGenerativeAIEmbeddings(model="gemini-embedding-2"), breakpoint_threshold_type="standard_deviation", breakpoint_threshold_amount=0)
print(splitter.split_text(text=text))