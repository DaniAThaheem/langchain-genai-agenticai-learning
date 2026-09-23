from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict



class CalculationState(TypedDict):
    a: int
    b: int
    c: int
    d: float

def calSqr(state: CalculationState):
    a = state['a']
    b = state['b']
    c = a**b
    return {"c":c}


def calSqrt(state: CalculationState):

    c = state['c']
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

final_state = workflow.invoke(init_state, config=config)

print(final_state)

print("________________________________________The State History_______________________________________________")

gen_history = workflow.get_state_history(config=config)
for h in gen_history:
    print(h)

print("________________________________________The State_______________________________________________")

print(workflow.get_state(config=config))

print("________________________________________Update State______________________________________________")

print(workflow.update_state(config={
    "configurable":{
        "thread_id": thread_id,
        "checkpoint_id": "1f1b75ec-0811-6546-8000-174f933749bf",
        "checkpoint_ns":""
    }
},
values={
    "a":4,
    "b":2
}
))
print("________________________________________The State History 1 Updated_______________________________________________")

gen_history = workflow.get_state_history(config=config)
for h in gen_history:
    print(h.values)

print("________________________________________The State History 2 Updated_______________________________________________")

final_state = workflow.invoke(None, config={
    "configurable":{
        "thread_id": thread_id,
        "checkpoint_id": "1f1b75ec-0811-6546-8000-174f933749bf",
        "checkpoint_ns":""
    }
})

print("________________________________________The State History 2 Updated_______________________________________________")
gen_history = workflow.get_state_history(config=config)
for h in gen_history:
    print(h.values)