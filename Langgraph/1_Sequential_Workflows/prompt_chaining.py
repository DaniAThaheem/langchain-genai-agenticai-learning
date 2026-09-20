from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict
from pydantic import BaseModel, Field

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

class CurrentState(TypedDict):
    title:str
    outline:str
    essay:str
    score: float

class ScoreSchema(BaseModel):
    score: float = Field(le=9.0, description="give the score less than or equal to 9 with float data type")

def generate_outline(state:CurrentState) -> CurrentState:
    title = state["title"]
    prompt= f'You are a professional essay writter. You check essays written to crack IELTS exams with high band. For example you define the mind map and metrics that help to write high band essays. Now you are writing essay for a person who is tring to learn how to crack the IELTS examination in writing part wiht high band. Do not try to give simple answers or people pleasing answers just put high standard and define the metrics and tricks that actually help and metters. Now generate the tricks that help to write the essay and  outline for the topic {title} '

    state["outline"] = model.invoke(prompt).content[0]['text']
    return state


def generate_essay(state:CurrentState) -> CurrentState:
    outline = state["outline"]
    prompt= f'You are a professional essay writter. You check essays written to crack IELTS exams with high band. For example you define the mind map and metrics that help to write high band essays. Now you are writing essay for a person who is tring to learn how to crack the IELTS examination in writing part wiht high band. Do not try to give simple answers or people pleasing answers just put high standard and define the metrics and tricks that actually help and metters. Now generate essay for topic with tricks {outline} '

    state["essay"] = model.invoke(prompt).content[0]['text']
    return state


def generate_score(state:CurrentState) -> CurrentState:
    outline = state["outline"]
    essay = state["essay"]

    prompt= f'You are a professional essay checker. You check essays written to crack IELTS exams with high band. For example you checck the mind map and metrics, outlines against the written essay that score these out of 9. Give the answer in floating point just like 6.0 or 4.0 or 7.5 etc. Now you are checking essay for a person who is tring to learn how to crack the IELTS examination in writing part wiht high band. Do not try to give simple answers or people pleasing answers just evaluate the score that actually help and matters. Now generate score for topic with tricks {outline} and essay {essay} out of 9.0. '

    structured_output_model =model.with_structured_output(ScoreSchema)

    state["score"] = structured_output_model.invoke(prompt).content[0]['text']
    return state


graph = StateGraph(CurrentState)

graph.add_node("generate_outline", generate_outline)
graph.add_node("generate_essay", generate_essay)
graph.add_node("generate_score", generate_score)

graph.add_edge(START, "generate_outline")
graph.add_edge("generate_outline", "generate_essay")
graph.add_edge("generate_essay", "generate_score")
graph.add_edge("generate_score", END)


workflow = graph.compile()

init_state = {"title":"Responsible AI"}

try:
    final_state = workflow.invoke(init_state)
    print(final_state)

except:
    print(final_state)