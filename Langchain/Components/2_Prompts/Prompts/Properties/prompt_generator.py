from langchain_core.prompts import PromptTemplate

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

#Accessing the generated file using the load_prompt()

prompt = template.save("prompt.json")