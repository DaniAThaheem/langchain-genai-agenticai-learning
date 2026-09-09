from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda
from typing import Literal
from pydantic import BaseModel, Field


load_dotenv()

model1 = ChatGoogleGenerativeAI(model="gemini-flash-latest")

parser1 = StrOutputParser()

class Review(BaseModel):
    sentiments: Literal["Pos", "Neg"] = Field(description="Classify the sentiment of the review")

parser2 = PydanticOutputParser(pydantic_object=Review)

prompt1 = PromptTemplate(
    template="Give the sentiment of the {review} \n {format_instruction}",
    input_variables=["review"],
    partial_variables={"format_instruction":parser2.get_format_instructions()}

)

prompt2 = PromptTemplate(
    template="Write a a propriate feedback of the positive {review}",
    input_variables=["review"]
)

prompt3 = PromptTemplate(
    template="Write a a propriate feedback of the negative {review}",
    input_variables=["review"]
)


classifier_chain = prompt1 | model1 | parser2

branch_chain = RunnableBranch(
    (lambda x: x.sentiments == "Pos", prompt2 | model1 | parser1),
    (lambda x: x.sentiments == "Neg", prompt3 | model1 | parser1),
    RunnableLambda(lambda x: "Could not find sentiment")
)

final_chain = classifier_chain | branch_chain

result = final_chain.invoke({"review": "this is terrible"})
print(result)