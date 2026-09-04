from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, load_prompt
import streamlit as st

load_dotenv()

#Accessing the generated file of prompt template using the load_prompt()
# template = load_prompt("template.json")

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

st.header("Research Summarizer")

paper_input = st.selectbox("Select Your Paper",["BERT: Pre-training of Deep Bidirectional Transformers","GPT-3: Language Models are few-shot learners","Diffusion Models Beat GANs on Image Synthesis","Attention is all you need"])
style_input = st.selectbox("Select Explanation Style",["Beginner-Friendly","Technical-Code Oriented","Mathematical"])
length_input = st.selectbox("Select Explantaion Length",["Short:(1-2 Paragraphs)","Medium:(2-3 Paragraphs)","Long: (Long Detailed Explannation)"])

template = PromptTemplate(
    template="""Please summarize the research paper titled "{paper_input}" with the following specifications:
     Explanation Style: {style_input}
     Explanation length: {length_input}
      1. Mathematical Details;
        - Include relevant mathimatical quations if present in the paper.
        - Explain the mathematical concepts using simple, intuitive code snippets where applicable
         
      2. Analogies:
        - Use relatable analogies to simplify complex ideas
     If certain inforation is not available in the paper, respond with: "Insufficient information
     Ensure the summary is clear, accurate, and aligned with the provided style and length """,
    input_variables=["paper_input", "style_input", "length_input"],
    validate_template=True
)

prompt = template.invoke({
    "paper_input":paper_input,
    "style_input":style_input,
    "length_input":length_input
    })

if st.button("Summarize"):
    result = model.invoke(prompt)
    st.write(result)