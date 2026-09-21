from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal


class EquationState(TypedDict):
    a: int
    b: int
    c: int
    equation: str
    descrimination: int
    result: str


def show_equation(state: EquationState):
    equation = f'{state["a"]}x2 + {state["b"] }x + {state["c"]} = 0'

    return {"equation":equation}


def calculate_descrimination(state: EquationState):
    a = state["a"]
    b = state["b"]
    c = state["c"]

    d= (b**2)-(4*a*c)

    return {"descrimination": d}


def condition_based_routing(state: EquationState) -> Literal["calculate_real_roots", "calculate_no_real_roots", "calculate_repeated_roots"]:
    d = state["descrimination"]
    if d>0 :
        return "calculate_real_roots"
    elif d == 0:
        return "calculate_repeated_roots"
    else:
        return "calculate_no_real_roots"

def calculating_real_roots(state: EquationState):
    d = state["descrimination"]
    root1 =(-state["b"]-(d)**0.5)/(2*state["a"])
    root2 =(-state["b"]+(d)**0.5)/(2*state["a"])

    result = f'The real roots of equation are {root1} and {root2}'
    return {"result":result}


def calculating_repeated_roots(state: EquationState):

    root =(-state["b"])/(2*state["a"])

    result = f'The repeated root of equation is {root}'
    return {"result":result}


def calculating_no_real_roots(state: EquationState):
   
    result = f'There are no real roots of equation'
    return {"result":result}

graph = StateGraph(EquationState)

graph.add_node("show_eq", show_equation)
graph.add_node("calculate_d", calculate_descrimination)
graph.add_node("calculate_real_roots", calculating_real_roots)
graph.add_node("calculate_repeated_roots", calculating_repeated_roots)
graph.add_node("calculate_no_real_roots", calculating_no_real_roots)

graph.add_edge(START, "show_eq")
graph.add_edge("show_eq", "calculate_d")
graph.add_conditional_edges("calculate_d", condition_based_routing)
graph.add_edge("calculate_real_roots", END)
graph.add_edge("calculate_repeated_roots", END)
graph.add_edge("calculate_no_real_roots", END)

workflow = graph.compile()

init_state = {"a":4, "b":7, "c":3}

final_state = workflow.invoke(init_state)

print(final_state)

