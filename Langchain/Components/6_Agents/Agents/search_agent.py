from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_classic import hub
from langchain_classic.agents import create_react_agent, AgentExecutor

load_dotenv()


search_tool = DuckDuckGoSearchRun()


llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")

prompt = hub.pull("hwchase17/react")


agent = create_react_agent(
    llm=llm,
    tools=[search_tool],
    prompt=prompt
)

agent_executer = AgentExecutor(
    agent=agent,
    tools=[search_tool],
    verbose=True
)


response = agent_executer.invoke({"input":"What is the current status about the impresonment of Imran Khan, and expected date of bail"})


print(response)

