from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

class ReviewState(TypedDict):
    review:str
    sentiment:str
    diagnosis_response:dict
    response:str


class SentimentSchema(BaseModel):
    sentiment:Literal["positive", "negative"] = Field(description="Generate the sentiment for the review")

class DiagnosisSchema(BaseModel):
    issueType: str = Field(description="Generate the issue type form the review")
    tone: str = Field(description="Tone of the review")
    urgency: str = Field(description="The urgency nature of the review")


structured_output_model_1 = model.with_structured_output(SentimentSchema)
structured_output_model_2 = model.with_structured_output(DiagnosisSchema)

def find_sentiments(state: ReviewState):
    review = state["review"]
    prompt = f'Find the sentiments of the given review \n {review}'
    result = structured_output_model_1.invoke(prompt).sentiment
    return {"sentiment":result}

def generate_positive_review(state: ReviewState):
    prompt = f'Generate a positive review for {state["review"]}'
    result = model.invoke(prompt).content[0]['text']
    return {"response":result}

def generate_diagnosis(state: ReviewState):
    prompt = f'Diagnosis the review for the issue type, tone and urgency for the review {state['review']}'
    result = structured_output_model_2.invoke(prompt)
    diagnosis_result = result.model_dump()
    return {"diagnosis_response":diagnosis_result}

def generate_negative_review(state: ReviewState):
    prompt = f'Generate a negative review for {state["review"]}'
    result = model.invoke(prompt).content[0]['text']
    return {"response":result}

def condition_based_routing(state: ReviewState) -> Literal["generate_positive_review", "generate_diagnosis"]:
    sentiment = state["sentiment"]
    if sentiment == "positive" :
        return "generate_positive_review"
    else:
        return "generate_diagnosis"

graph = StateGraph(ReviewState)

graph.add_node("find_sentiments", find_sentiments)
graph.add_node("generate_positive_review", generate_positive_review)
graph.add_node("generate_diagnosis", generate_diagnosis)
graph.add_node("generate_negative_review", generate_negative_review)

graph.add_edge(START, "find_sentiments")
graph.add_conditional_edges("find_sentiments", condition_based_routing)
graph.add_edge("generate_positive_review", END)
graph.add_edge("generate_diagnosis","generate_negative_review")
graph.add_edge("generate_negative_review", END)

workflow = graph.compile()

init_state = {"review":"I try to login to the national job portal but it says you are already register but it did not used my cnic"}

final_state = workflow.invoke(init_state)

print(final_state)


