from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langgraph.checkpoint.memory import MemorySaver



class CalculationState(TypedDict):
    a: int
    b: int
    c: int

def calculation(state: CalculationState):
    a = state['a']
    b= state['b']

    c = a**b
    return {"c":c}


graph = StateGraph(CalculationState)
graph.add_node("calculation", calculation)

graph.add_edge(START, "calculation")
graph.add_edge("calculation", END)

checkpointer = MemorySaver()

workflow = graph.compile(checkpointer=checkpointer)

init_state = {"a":4, "b":2}

thread_id = "`12345"

config = {
    "configurable":{
        "thread_id":thread_id
    }
}

final_state = workflow.invoke(init_state, config=config)

print(final_state)

print(workflow.get_state(config=config))
print(workflow.get_state_history(config=config))