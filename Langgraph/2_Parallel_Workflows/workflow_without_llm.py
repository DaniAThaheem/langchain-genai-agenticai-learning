from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class MatchState(TypedDict):
    scores: int
    sixes: int
    fours: int
    balls: int
    strike_rate: float
    ball_per_boundaries: float
    boundaries_percent: float
    summary: str


def calculate_strike_rate(state: MatchState):
    sr = (state['scores'] / state['balls']) * 100
    return {"strike_rate": sr}

def calculate_bpb(state: MatchState):
    bpb = state['balls']/(state['sixes'] + state['fours'])
    return {"ball_per_boundaries":bpb}

def calculate_boundaries_percent(state: MatchState):
    bp =(((state['fours']*4)) + (state['sixes']*6)/state['scores']) * 100
    return {"boundaries_percent":bp}

def show_summary(state: MatchState):
    return {"summary" :f'Strike Rate: {state["strike_rate"]}, Ball per Boundaries: {state['ball_per_boundaries']}, Boundaries Percent: {state['boundaries_percent']}'}



graph = StateGraph(MatchState)

graph.add_node("calculate_sr", calculate_strike_rate)
graph.add_node("calculate_bpb", calculate_bpb)
graph.add_node("calculatee_bp", calculate_boundaries_percent)
graph.add_node("summary", show_summary)

graph.add_edge(START, "calculate_sr")
graph.add_edge(START, "calculate_bpb")
graph.add_edge(START, "calculatee_bp")

graph.add_edge("summary", "calculate_sr")
graph.add_edge("summary", "calculate_bpb")
graph.add_edge("summary", "calculatee_bp")

graph.add_edge("summary", END)

workflow = graph.compile()

init_state = {
    "sixes":6,
    "fours":4,
    "scores": 88,
    "balls": 60
}

final_state = workflow.invoke(init_state)

print(final_state)

