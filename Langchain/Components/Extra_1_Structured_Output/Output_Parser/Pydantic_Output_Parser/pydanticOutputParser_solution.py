from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

llm = HuggingFaceEndpoint(
    repo_id="",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

class MobileSpecification:
    launch: str= Field(description="Launch data of device")
    colors:list[str] = Field(description="List of colors available for device")
    os_supported: str = Field(description="Which os support this mobile")
    chipset: str = Field(description="Chipset supported by the mobile")
    ram : list[str] = Field(description="Which RAM variant are available")

pydantic_outputparser = PydanticOutputParser(pydantic_object=MobileSpecification)

chat_template = PromptTemplate(
    template="Give the specifications of {mobile_model} \n {format_instruction}" ,
    input_variables=["mobile_model"],
    partial_variables={"format_instruction":pydantic_outputparser.get_format_instructions()}
)

chain = chat_template | model | pydantic_outputparser

final_result = chain.invoke({"mobile_model":"OPPO A76"})

# prompt = chat_template.invoke({})

# result = model.invoke(prompt)

# final_result = json_outputparser.parse(result.content)

print(final_result)



