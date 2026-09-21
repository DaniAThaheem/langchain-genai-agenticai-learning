from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated, Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
import operator

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")


class TweetState(TypedDict):
    topic: str
    tweet: str
    evaluation_result: str
    feedback:str
    iteration_count: int
    max_iteration: int
    tweet_history: Annotated[list[str], operator.add]

class EvaluationSchema(BaseModel):
    evaluation_result: Literal["approved", "rejected"] = Field(description="Evalution result of the tweet")
    feedback: str = Field(description="Feedback about the result")

structured_output_model = model.with_structured_output(EvaluationSchema)

def generate_tweet(state: TweetState):
    prompt = f'Generate a funny, meme mode, original tweet about the topic {state["topic"]}'
    result = model.invoke(prompt).content[0]['text']
    return {"tweet":result, "tweet_history":list[result]}

def evaluate_tweet(state: TweetState):
    prompt = f'Evaluate the tweet based on the virality and humour {state["tweet"]}'
    result = structured_output_model.invoke(prompt)
    return {"evaluation_result":result.evaluation_result, "feedback":result.feedback}

def optimize_tweet(state: TweetState):
    prompt = f'Optimize the tweet w.r.t feedback {state["feedback"] } for the tweet {state['tweet']} and the topic is {state["topic"]} '
    result = model.invoke(prompt).content[0]['text']
    return {"tweet":result, "iteration_count":state["iteration_count"]+1, "tweet_history":list[result]}

def condition_based_routing(state: TweetState) -> Literal["approved", "rejected"]:
    if state["iteration_count"] >= state["max_iteration"] or state["evaluation_result"] == "approved":
        return "approved"
    else:
        return "rejected"


graph = StateGraph(TweetState)

graph.add_node("generate_tweet", generate_tweet)
graph.add_node("evaluate_tweet", evaluate_tweet)
graph.add_node("optimize_tweet", optimize_tweet)

graph.add_edge(START, "generate_tweet")
graph.add_edge("generate_tweet", "evaluate_tweet")
graph.add_conditional_edges("evaluate_tweet", condition_based_routing, {"approved": END, "rejected":"optimize_tweet"})
graph.add_edge("optimize_tweet", "evaluate_tweet")

workflow = graph.compile()

init_state = {"topic":"Pakistani Army"}

final_state = workflow.invoke(init_state)

print(final_state)

