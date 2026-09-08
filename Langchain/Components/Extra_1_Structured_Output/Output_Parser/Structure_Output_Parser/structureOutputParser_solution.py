from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = HuggingFaceEndpoint(
    repo_id="",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

json_outputparser = JsonOutputParser

chat_template = PromptTemplate(
    template="Give the specifications of OPPO A76 \n {format_instruction}" ,
    input_variables=[],
    partial_variables={"format_instruction":json_outputparser.get_format_instructions()}
)

chain = chat_template | model | json_outputparser

final_result = chain.invoke({})

# prompt = chat_template.invoke({})

# result = model.invoke(prompt)

# final_result = json_outputparser.parse(result.content)

print(final_result)



