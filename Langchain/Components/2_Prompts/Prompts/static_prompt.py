from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-flash-latest")
st.header("Research Summarizer")
user_input = st.text_input("Enter you prompt")
if st.button("Summarize"):
    result = model.invoke(user_input)
    st.write(result)
