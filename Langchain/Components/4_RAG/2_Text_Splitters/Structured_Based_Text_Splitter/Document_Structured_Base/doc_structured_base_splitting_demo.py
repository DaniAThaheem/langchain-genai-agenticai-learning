from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

text = """
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 0
)

result = splitter.split_text(text=text)

print(result)
"""

splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size = 100,
    chunk_overlap = 0
    
)

result = splitter.split_text(text=text)

print(result)