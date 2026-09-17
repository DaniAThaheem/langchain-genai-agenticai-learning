from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_classic.agents import create_react_agent, AgentExecutor
import requests

load_dotenv()


@tool
def get_weather(city:str)->str:
    """This tool takes the name of the city and returns the weather information of that city"""
    url = f'https://api.weatherstack.com/current?access_key=2d1e039103e1c73bcfe3680de45ec022&query={city}'
    response = requests.get(url)
    return response.json()


search_tool = DuckDuckGoSearchRun()


llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")

prompt = PromptTemplate.from_template(template="""
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
""")

agent = create_react_agent(
    llm=llm,
    tools=[search_tool, get_weather],
    prompt=prompt
)

agent_executer = AgentExecutor(
    agent=agent,
    tools=[search_tool, get_weather],
    verbose=True
)


response = agent_executer.invoke({"input":"Which is the capital of Pakistan and find its current weather conditions?"})


print(response)

