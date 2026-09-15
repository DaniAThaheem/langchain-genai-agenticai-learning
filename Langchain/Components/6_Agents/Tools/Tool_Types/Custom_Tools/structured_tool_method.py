from langchain_community.tools import StructuredTool
from pydantic import BaseModel, Field

class Schema(BaseModel):
    a: int = Field(description="First number for multiplication")
    b: int = Field(description="Second number for multiplication")


def multiply(a:int, b:int) -> int:
    return a*b

multiplication_tool = StructuredTool.from_function(
    func=multiply,
    name="Multiplication",
    description="Multiply two numbers",
    args_schema=Schema
)

result = multiplication_tool.invoke({"a":2, "b":3})
print(result)