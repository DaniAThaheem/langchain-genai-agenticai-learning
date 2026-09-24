import streamlit as st

user_input = st.chat_input("Type here...")

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input:
    with st.chat_message("user"):
        st.session_state["message_history"].append({"role":"human", "content":user_input})
        st.write(user_input)

    with st.chat_message("assistant"):
        st.session_state["message_history"].append({"role":"assistant", "content":user_input})
        st.write(user_input)


    