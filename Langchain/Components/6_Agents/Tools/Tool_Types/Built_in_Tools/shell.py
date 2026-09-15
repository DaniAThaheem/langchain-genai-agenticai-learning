from langchain_community.tools import ShellTool

shell = ShellTool()
result = shell.invoke("whoami")
print(result)