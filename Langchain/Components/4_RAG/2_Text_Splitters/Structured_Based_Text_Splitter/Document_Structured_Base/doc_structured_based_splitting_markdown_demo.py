from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

text = """
### Standardizing the Components. 
### Creating Chain of Multiple Chains.
This is the LLM class where there is a predict method which is mocked to give the response to a prompt
"""


splitter= RecursiveCharacterTextSplitter.from_language(
    language = Language.MARKDOWN,
    chunk_size = 50,
    chunk_overlap = 0
)

result = splitter.split_text(text=text)

print(result)