import streamlit as st
from langgraph_chatbot_backend import workflow
from langchain_core.messages import HumanMessage

user_input = st.chat_input("Type here...")

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
        st.session_state["message_history"].append({"role":"human", "content":user_input})
        st.write(user_input)
        init_state = {"messages":[HumanMessage(content=input)]}
        ai_output = workflow.invoke(init_state, config=config)

    with st.chat_message("assistant"):
        st.session_state["message_history"].append({"role":"assistant", "content":ai_output[-1].content})
        st.write(ai_output[-1].content)


    