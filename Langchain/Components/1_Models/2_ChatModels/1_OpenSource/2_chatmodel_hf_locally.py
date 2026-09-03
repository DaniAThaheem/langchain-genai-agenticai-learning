from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
import os

os.environ["HF_HOME"] = "D:\HF_Cache"
llm = HuggingFacePipeline.from_model_id(
    model_id="meta-llama/Llama-3.1-8B-Instruct"
)
model = ChatHuggingFace(llm=llm)
result = model.invoke("How to maximize the chances of getting Erasmus Mundis Scholarship?")
print(result)
print(result.content)