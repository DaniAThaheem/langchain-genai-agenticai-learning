from langchain_core.tools import tool

@tool
def multiply (a:int, b:int)->int:
    """Multiplying two numbers"""
    return a*b

@tool
def add (a:int, b:int)->int:
    """Adding two numbers"""
    return a+b


class MathToolkit :
    def get_tools(self):
        return [multiply, add]


math_toolkit = MathToolkit()
tools = math_toolkit.get_tools()
for tool in tools:
    print(tool.name + "-->" +tool.description)