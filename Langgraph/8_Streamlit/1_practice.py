import streamlit as st

st.title("Programming Language Picker")
st.subheader("You will have options to pick different programming languages")
st.text("Which programming language you choose is the main point to analyze your ability to tell the team that you have potential to grow in that field. And we believe that all you abilities to go through these framework are heavily dependent on you programming language skill")

language = st.selectbox("Please select you programming language:", ["JS", "Java", "Python", "C", "C#", "C++"])

st.success("You have selected a programming language successfully")

st.write(f"You have an excellent choice. {language}, a choice to say wao")

