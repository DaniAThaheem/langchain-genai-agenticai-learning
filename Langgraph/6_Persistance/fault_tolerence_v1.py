from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict
import time


class CalculationState(TypedDict):
    a: int
    b: int
    c: int
    d: float

def calSqr(state: CalculationState):
    a = state['a']
    b = state['b']
    time.sleep(2)
    c = a**b
    return {"c":c}


def calSqrt(state: CalculationState):

    c = state['c']
    time.sleep(3)
    d = c**0.5
    return {"d": d}

graph = StateGraph(CalculationState)

graph.add_node("calSqr", calSqr)
graph.add_node("calSqrt", calSqrt)

graph.add_edge(START, "calSqr")
graph.add_edge("calSqr", "calSqrt")
graph.add_edge("calSqrt", END)

checkpointer = MemorySaver()

workflow = graph.compile(checkpointer=checkpointer)

init_state = {"a":2, "b":2}

thread_id = "2345abc"

config = {
    "configurable":{
        "thread_id": thread_id
    }
}

# final_state = workflow.invoke(init_state, config=config)

# print(final_state)

print("________________________________________The State History_______________________________________________")

gen_history = workflow.get_state_history(config=config)
for h in gen_history:
    print(h)

print("________________________________________The State_______________________________________________")

print(workflow.get_state(config=config))