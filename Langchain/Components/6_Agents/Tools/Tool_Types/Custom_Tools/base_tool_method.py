from langchain_community.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class Schema(BaseModel):
    a: int = Field(required = True, description="First number for multiplication")
    b: int = Field(required = True, description="Second number for multiplication")

class Multiplication(BaseTool):
    name: str ="Multiplication"
    description: str ="Multiply two numbers"
    args_schema: Type[BaseModel] = Schema

    def _run(self, a:int, b:int) ->int:
        return a*b





multiply_tool = Multiplication()
result = multiply_tool.invoke({"a":2, "b":6})
print(result)
print(multiply_tool.name)
print(multiply_tool.description)
print(multiply_tool.args)
