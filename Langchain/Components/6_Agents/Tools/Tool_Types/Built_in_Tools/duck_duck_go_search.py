from langchain_community.tools import DuckDuckGoSearchRun

duckduckgo = DuckDuckGoSearchRun()
result = duckduckgo.invoke("Imran Khan as a politian")
print(result)