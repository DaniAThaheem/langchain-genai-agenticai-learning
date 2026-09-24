from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, BaseMessage
from typing import TypedDict, Annotated

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

checkpointer = MemorySaver()

workflow = graph.compile(checkpointer=checkpointer)

