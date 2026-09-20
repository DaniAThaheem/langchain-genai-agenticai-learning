from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv 
from typing import TypedDict

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")



class CurrentState(TypedDict):
    question:str
    answer:str


def llm_call(state: CurrentState) -> CurrentState:
    question = state["question"]
    prompt = f'You are a professional journalist who is expert in talking about the current affairs of technology from multiple perspective.For example: You explain about the the iphone, huawei and samsung with respect to cost geopolitical positions, countries direction in term of control over data and privacy and countries intention to control over the world. You are working for a person who is trying to understand the underneath game not the appeared point of view or intention of every thing. Do not try to manipulate with false fact. If the info is not available just simple say a big no. Do not try to be american or any other countries representative. Stay neutral and only true facts. The question is {question}'

    result = model.invoke(prompt)
    state["answer"] = result.content[0]['text']
    return state


graph = StateGraph(CurrentState)

graph.add_node("llm_call", llm_call)

graph.add_edge(START, "llm_call")

graph.add_edge("llm_call", END)

workflow =graph.compile()

init_state = {"question":"Why are American AI companies asking to slow down the AI Development speed like the previous statements from the CEO of Antropic, Elon Musk, Sam Altman, while Nvidia CEO made a contract with the Hugging Face?"}

final_state = workflow.invoke(init_state)

print(final_state)

