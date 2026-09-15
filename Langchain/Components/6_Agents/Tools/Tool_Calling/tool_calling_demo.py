from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

# Tool Creation

@tool
def multiply(a: int, b: int) -> int:
    "Multiply two numbers a and b"
    return a * b

# Tool Binding
model = ChatGoogleGenerativeAI(model="gemini-flash-latest")
model_with_tools = model.bind_tools([multiply])

# Tool Calling
messages = [HumanMessage(content="Can you multiply 8 and 9")]
model_result = model_with_tools.invoke(messages)
messages.append(model_result)

tool_call = model_result.tool_calls[0]

# Tool Execution
tool_result = multiply.invoke(tool_call["args"])
messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"]))

print(messages)

final_result = model_with_tools.invoke(messages)
print(final_result)


