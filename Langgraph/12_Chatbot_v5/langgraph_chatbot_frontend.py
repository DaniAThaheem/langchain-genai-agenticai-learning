import streamlit as st
from langgraph_chatbot_backend import workflow, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid

user_input = st.chat_input("Type here...")

def addThreadId(thread_id):
    if thread_id not in st.session_state["thread_list"]:
        st.session_state["thread_list"].append(thread_id) 

def load_conversation(thread_id):
    return workflow.get_state(config={
        "configurable":{
            "thread_id":thread_id
        }
    }).values["messages"]

def genThreadId():
    return uuid.uuid4()

def reset_chat():
    st.session_state["thread_id"] = genThreadId()
    st.session_state["message_history"] = []
    addThreadId(st.session_state["thread_id"])



if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = genThreadId()

if "thread_list" not in st.session_state:
    st.session_state["thread_list"] = retrieve_all_threads()

addThreadId(st.session_state["thread_id"])

config = {
        "configurable":{
            "thread_id":st.session_state["thread_id"]
        }
    }


st.sidebar.title("History")

if st.sidebar.button("New Chat", width=270):
    reset_chat()

st.sidebar.subheader("Conversations")

for thread_id in st.session_state["thread_list"][::-1]:
    if st.sidebar.button(thread_id):
        messages = load_conversation(thread_id)
        msg_history =[]
        for message in messages:
            if isinstance(message, HumanMessage):
                role= "user"
                msg_history.append({"role":role, "content":message.content})
            else:
                role= "assistant"
                msg_history.append({"role":role, "content":message.content})
        st.session_state["message_history"] = msg_history


for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input:
    with st.chat_message("user"):
        st.session_state["message_history"].append({"role":"human", "content":user_input})
        st.write(user_input)
        init_state = {"messages":[HumanMessage(content=user_input)]}

    with st.chat_message("assistant"):
        ai_output = st.write_stream(
            message_chunk.content for message_chunk,  in workflow.stream(init_state, config=config, stream_mode="messages")
        )
        
        st.session_state["message_history"].append({"role":"assistant", "content":ai_output})



    