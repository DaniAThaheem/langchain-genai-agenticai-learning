# What is actually happening is that we often face issues with models which can not generate the structured output. We use output parser. Now when using the chain feeding output of llm again to the llm is a common phenomenon. So instead of getting the unstructured output we use output parsers to get required output.


from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

llm = HuggingFaceEndpoint(
    repo_id="",
    task="text-generation"
)
model = ChatHuggingFace(llm=llm)

chat_template1 = PromptTemplate(
    template=" Write a detailed note about the topic {topic}",
    input_variables=["topic"]
)

chat_template2 = PromptTemplate(
    template="Write a 5 lines summary of the topic {text}",
    input_variables=["text"]
)


promp1 = chat_template1.invoke({"topic":"A student from village facing difficulties in modern era and how to compete witht the students of advanced city in the race of Technology."})

result_prompt_1 = model.invoke(promp1)

prompt2 = chat_template2.invoke({"text":result_prompt_1.content})

result_prompt_2 = model.invoke(prompt2)

print(result_prompt_2.content)



