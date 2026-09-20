from langgraph.graph import StateGraph, START, END
from typing import TypedDict

#For BMI, we have weight and heigh and the body mass index

class BMIState(TypedDict):
    weight_kg: float
    height_m: float
    bmi: float


def bmi_calculation(state: BMIState) -> BMIState:
    weight = state["weight_kg"] 
    height = state["height_m"]

    state["bmi"] = round(weight/(height**2), 2)
    return state



graph = StateGraph(BMIState)

graph.add_node("bmi", bmi_calculation)

graph.add_edge(START, "bmi")

graph.add_edge("bmi", END)

workflow=graph.compile()

init_state = {"weight_kg":55, "height_m":1.73}

final_state = workflow.invoke(init_state)

print(final_state)

