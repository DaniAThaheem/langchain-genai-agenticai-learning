from langchain_core.tools import tool

@tool
def multiply (a:int, b:int)->int:
    """Multiplying two numbers"""
    return a*b

result = multiply.invoke({"a":4,"b":6})
print(result)
print(multiply.name)
print(multiply.description)
print(multiply.args)