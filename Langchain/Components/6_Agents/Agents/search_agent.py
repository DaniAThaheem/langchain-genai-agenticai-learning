from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_classic import hub
from langchain_classic.agents import create_react_agent, AgentExecutor
import requests

load_dotenv()


@tool
def get_weather(city:str)->object:
    """This tool takes the name of the city and returns the weather information of that city"""
    url = f'https://api.weatherstack.com/current?access_key=4d1d8ae207a8c845a52df8a67bf3623e&query={city}'
    response = requests.get(url)
    return response.json()


search_tool = DuckDuckGoSearchRun()


llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")

prompt = hub.pull("hwchase17/react")


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

