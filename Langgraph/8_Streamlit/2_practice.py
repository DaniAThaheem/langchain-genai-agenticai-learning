import streamlit as st

st.title("Widgets Practice")


language_ur = st.checkbox("Urdu")
language_eng = st.checkbox("English")

st.radio("Gender: ", ["Male", "Female"])

if st.button("Click Me"):
    st.success("You clicked")

value = st.text_input("Enter value")
if value:
    st.write(value)
