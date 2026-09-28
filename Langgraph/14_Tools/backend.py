from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, BaseMessage
from typing import TypedDict, Annotated
import sqlite3
from langchain_community.tools import DuckDuckGoSearchRun, tool
import requests
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

search = DuckDuckGoSearchRun()

@tool
def search_weather(city:str):
    """
    Get the weather of the city by passing the city name
    """

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=c6264f5b47c23a53621b736b6542cb5f"
    r = requests.get(url)
    return r.json()


tool_list = [search, search_weather]

llm_with_tools = model.bind_tools(tools=tool_list)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat(state:ChatState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


tool_list_node  =ToolNode(tool_list)


graph = StateGraph(ChatState)

graph.add_node("chat_node", chat)
graph.add_node("tool_node", tool_list_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges(
    "chat_node",
    tools_condition,
    {"tools": "tool_node", END: END},
)
graph.add_edge("tool_node", "chat_node")

conn = sqlite3.connect(database="chat.db", check_same_thread=False)

checkpointer = SqliteSaver(conn)
checkpointer.setup()

workflow = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)
