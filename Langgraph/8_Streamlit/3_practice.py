import streamlit as st


st.title("Implementing Layout Concepts")

col1, col2 = st.columns(2)

def open_sidebar():
    st.sidebar.subheader("History")
    st.sidebar.button("New Chat")
    st.sidebar.markdown("### Previous Chats")

with col1:
    st.subheader("We are here to listen you")
    clicked_new_chat = st.button("New Chat", width=200,)

with col2:
    st.subheader("Explore previous history")
    clicked_open_sidebar = st.button("History", width=200, on_click=open_sidebar)