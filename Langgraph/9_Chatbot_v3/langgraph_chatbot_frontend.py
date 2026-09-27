import streamlit as st
from langgraph_chatbot_backend import workflow
from langchain_core.messages import HumanMessage

user_input = st.chat_input("Type here...")

def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block["text"]
            for block in content
            if isinstance(block, dict)
            and block.get("type") == "text"
            and isinstance(block.get("text"), str)
        )
    return ""

thread_id = "123abc"
config = {
        "configurable":{
            "thread_id":thread_id
        }
    }

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input:
    with st.chat_message("user"):
        st.session_state["message_history"].append({"role":"user", "content":user_input})
        st.write(user_input)
        init_state = {"messages":[HumanMessage(content=user_input)]}

    with st.chat_message("assistant"):
        ai_output = st.write_stream(
            text
            for message_chunk, _ in workflow.stream(
                init_state, config=config, stream_mode="messages"
            )
            if (text := extract_text(message_chunk.content))
        )
        
        st.session_state["message_history"].append({"role":"assistant", "content":ai_output})



    