from langgraph.graph import StateGraph, START, END, add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, BaseMessage
from typing import TypedDict, Annotated
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import ToolNode, tools_condition
from mcp_server_config import SERVER
import asyncio

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

client = MultiServerMCPClient(SERVER)


async def build_graph():

    tool_list = await client.get_tools()

    llm_with_tools = model.bind_tools(tools=tool_list)


    # 1. Define your ChatState properly
    class ChatState(TypedDict):
        messages: Annotated[list[BaseMessage], add_messages]    # The raw user prompt string
        # The list tracking LLM/Tool outputs

    # 2. Update your chat node function
    async def chat(state: ChatState):
        user_prompt = state["messages"]
        response = await llm_with_tools.ainvoke(user_prompt)
        
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


    workflow = graph.compile()

    return workflow

async def main():
    workflow = await build_graph()
    init_state = {"messages":[HumanMessage(content="Show the all expense")]}
    result = await workflow.ainvoke(input= init_state)
    print(result)

if __name__ == "__main__":

    asyncio.run(main())
