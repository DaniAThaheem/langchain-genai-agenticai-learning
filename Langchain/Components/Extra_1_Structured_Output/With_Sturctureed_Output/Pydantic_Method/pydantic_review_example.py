from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional, Literal

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

class Review(BaseModel):
    key_themes: list[str] = Field(description="Write all the temes in a list in string form")
    summary: str = Field(description="Write down a summary of the review")
    sentiments: Literal["Pos", "Neg"] = Field(description="Write down the sentiments in literal Pos or Neg")
    pros: Optional[list[str]] = Field(default=None, description="Write down the list of pros if available in the review")
    cons: Optional[list[str]] = Field(default=None, description="Write down the list of cons if available in the review")
    name: Optional[str] = Field(default=None, description="Write down the name of the person who wrote the review")

structured_model = model.with_structured_output(Review)
result = structured_model.invoke("""
I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it's an absolute powerhouse! The Snapdragon 8 Gen 3 processor makes everything lightning fast-whether I'm gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.
The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. What really blew me away is the 200MP camera-the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.
However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung's One UI still comes with bloatware-why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow.
Pros:
Insanely powerful processor (great for gaming and productivity)
Stunning 200MP camera with incredible zoom capabilities
Long battery life with fast charging
S-Pen support is unique and useful
Cons:
Bulky and heavy-not great for one-handed use
Bloatware still exists in One UI
Expensive compared to competitors
Would you like me to summarize these points, or do you need help formatting this text into a specific style?
""")


print(result)