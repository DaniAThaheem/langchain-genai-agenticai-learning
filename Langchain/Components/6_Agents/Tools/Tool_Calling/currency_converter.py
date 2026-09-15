from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
import requests
import json
import os

load_dotenv()


# Tool Creation
@tool
def conversion_factor(base_currency: str, target_currency: str):
    """Get the conversion rate between two currencies."""
    url = f"https://v6.exchangerate-api.com/v6/a6c4a38db240ab6761dd912f/pair/{base_currency}/{target_currency}"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    data = response.json()

    if data.get("result") != "success":
        raise ValueError(f"Exchange rate API error: {data}")

    return {
        "base_currency": base_currency,
        "target_currency": target_currency,
        "conversion_rate": data["conversion_rate"],
    }


@tool
def converter(base_currency_value: int, conversion_rate: float) -> float:
    """Multiply base currency value by conversion rate."""
    return float(base_currency_value) * float(conversion_rate)


# Tool Binding
model = ChatGoogleGenerativeAI(model="gemini-flash-latest")
model_with_tools = model.bind_tools([conversion_factor, converter])

# Tool Calling
messages = [HumanMessage(content="I want conversion of PKR to USD. How much USD will be in 30000?")]
ai_message = model_with_tools.invoke(messages)
messages.append(ai_message)

print(ai_message)

conversion_rate = None

for tool_call in ai_message.tool_calls:
    if tool_call["name"] == "conversion_factor":
        tool_args = tool_call["args"]
        result = conversion_factor.invoke(tool_args)
        print(result)

        messages.append(ToolMessage(content=json.dumps(result), tool_call_id=tool_call["id"]))
        conversion_rate = result["conversion_rate"]

    if tool_call["name"] == "converter":
        tool_call["args"]["conversion_rate"] = conversion_rate
        result = converter.invoke(tool_call["args"])
        print(result)
        messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))

res = model_with_tools.invoke(messages)
print(res)





