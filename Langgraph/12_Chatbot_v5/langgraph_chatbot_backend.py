from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, BaseMessage
from typing import TypedDict, Annotated
import sqlite3

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat(state:ChatState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"message": messages[response]}


graph = StateGraph(ChatState)

graph.add_node("chat", chat)

graph.add_edge(START, "chat")
graph.add_edge("chat", END)

conn = sqlite3.connect(database="chat.db", check_same_thread=False)

checkpointer = MemorySaver()

workflow = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)
