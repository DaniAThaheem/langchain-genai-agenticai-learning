from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
import operator

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")

class EssayState(TypedDict):
    essay: str
    clarity_feedback: str
    analysis_feedback: str
    language_feedback: str
    overall_feedback: str
    individual_score: Annotated[ list[int], operator.add] 
    average_score: float


class EssaySchema(BaseModel):
    feedback: str = Field(description="Detailed feedback about the essay")
    score: int = Field(le=0, ge=10, description="Score the essay between the 0 and 10 in integer form")


def get_clarity_feedback(state: EssayState):

    essay = state['essay']

    prompt= f'You are a professional essay checker. You check essays written to crack IELTS exams with high band. For example you check clarity of thought against the written essay that score these out of 10. Give the answer in int just like 6 or 4 or 7 etc. Now you are checking essay for a person who is tring to learn how to crack the IELTS examination in writing part wiht high band. Do not try to give simple answers or people pleasing answers just evaluate the score that actually help and matters. Now generate score for essay {essay} and generate a detailed feedback'
    structured_output_model = model.with_structured_output(EssaySchema)
    result = structured_output_model.invoke(prompt)
    return {
        "clarity_feedback": result.feedback,
        "individual_score": [result.score]
    }
def get_analysis_feedback(state: EssayState):

    essay = state['essay']

    prompt= f'You are a professional essay checker. You check essays written to crack IELTS exams with high band. For example you check depth of analysis against the written essay that score these out of 10. Give the answer in int just like 6 or 4 or 7 etc. Now you are checking essay for a person who is tring to learn how to crack the IELTS examination in writing part wiht high band. Do not try to give simple answers or people pleasing answers just evaluate the score that actually help and matters. Now generate score for essay {essay} and generate a detailed feedback'
    structured_output_model = model.with_structured_output(EssaySchema)
    result = structured_output_model.invoke(prompt)
    return {
        "analysis_feedback": result.feedback,
        "individual_score": [result.score]
    }
def get_clarity_feedback(state: EssayState):

    essay = state['essay']

    prompt= f'You are a professional essay checker. You check essays written to crack IELTS exams with high band. For example you check clarity of thought against the written essay that score these out of 10. Give the answer in int just like 6 or 4 or 7 etc. Now you are checking essay for a person who is tring to learn how to crack the IELTS examination in writing part wiht high band. Do not try to give simple answers or people pleasing answers just evaluate the score that actually help and matters. Now generate score for essay {essay} and generate a detailed feedback'
    structured_output_model = model.with_structured_output(EssaySchema)
    result = structured_output_model.invoke(prompt)
    return {
        "language_feedback": result.feedback,
        "individual_score": [result.score]
    }


def show_summary(state: EssayState):
    clarity_feedback = state['clarity_feedback']
    analysis_feedback = state["analysis_feedback"]
    language_feedback = state['language_feedback']


    prompt = f'Give the overall feedback according to the different feedback from the different models {clarity_feedback},  {analysis_feedback} and {language_feedback}'

    result = model.invoke(prompt)

    average_score = sum(state['individual_score'])/ len(state["individual_score"])

    return {
        "overall_feedback": result.content[0]['text'],
        "average_score":average_score

    }



graph = StateGraph(EssayState)

graph.add_node("clarity_feedback", get_clarity_feedback)
graph.add_node("analysis_feedback", get_analysis_feedback)
graph.add_node("language_feedback", get_analysis_feedback)
graph.add_node("summary", show_summary)


graph.add_edge(START, "clarity_feedback")
graph.add_edge(START, "analysis_feedback")
graph.add_edge(START, "language_feedback")

graph.add_edge("clarity_feedback", "summary")
graph.add_edge("analysis_feedback", "summary")
graph.add_edge("language_feedback", "summary")

graph.add_edge("summary", END)

workflow = graph.compile()

init_state ={
    "essay":"""
To understand the apparent contradiction between American AI lab leaders calling for pauses/regulations and hardware giants like Nvidia aggressively expanding open-source distribution through Hugging Face, you have to look past the moral and philosophical rhetoric of “AI safety.” 
What appears on the surface as ideological division is, in reality, a structural conflict between **software layer monopolists** and the **hardware layer monopoly**.
Here is an objective breakdown of the incentives, the market mechanics, and the geopolitical chess game taking place beneath the surface.\n\n---\n\n### 
1. The Software Frontier: Altman, Amodei, and Musk\n*(The Strategy: Regulatory Capture and Moat Construction)*\n\nWhen Sam Altman (OpenAI), Dario Amodei (Anthropic), and Elon Musk (xAI/Tesla) speak before the U.S. Congress, sign open letters calling to "slow down" or "pause" large-scale AI development, or call for regulatory licensing, their motivations are shaped by distinct corporate imperatives:\n\n#### 
A. Regulatory Capture (Building the Moat)\nBuilding a frontier Foundation Model costs hundreds of millions—soon billions—of dollars. However, the open-source community (Meta’s Llama series, Mistral, independent researchers) quickly began catching up to proprietary models throughout 2023 and 2024.\n* **The threat:** If small startups or decentralized developers can achieve 90% of GPT-4’s performance using low-cost fine-tuning, the proprietary models lose their enterprise pricing power.\n* **The solution:** Advocate for safety regulations based on **compute thresholds** (e.g., any model trained using more than $10^{26}$ FLOPS must be licensed, audited, and cleared by the government). \n* **The result:** Startups and open-source foundations cannot afford the legal, compliance, and auditing overhead. Incumbents like OpenAI, Google, and Anthropic cement their positions as an oligopoly of "licensed operators"—much like pharmaceutical giants or major defense contractors.\n\n#### 
B. Deflection from Present Liability to Future Catastrophe\nFrontier labs face immediate, multi-billion-dollar legal liabilities right now:\n* Copyright infringement lawsuits (training on proprietary data without permission).\n* Data privacy violations (GDPR in Europe, CCPA in California).\n* Antitrust scrutiny regarding their close ties to Microsoft, Amazon, and Google.\n\nBy focusing public and legislative attention on **hypothetical existential threats** (e.g., "AI causing human extinction" or "bioweapons"), these executives steer the conversation away from mundane, near-term issues like copyright law, fair use, and monopolistic pricing. It is politically safer to debate a fictional apocalypse in 20 years than to settle copyright suits worth billions today.\n\n#### 
C. Elon Musk’s Specific Vector: The Asymmetric Pause\nElon Musk famously signed the Future of Life Institute’s open letter in March 2023 calling for a 6-month pause on models stronger than GPT-4.\n* During that very same window, corporate filings revealed that Musk was procuring thousands of Nvidia H100 GPUs and incorporating his own competing entity, **xAI**.\n* For an entrepreneur lagging behind the OpenAI-Microsoft and Anthropic-Google alliances, a industry-wide "pause" would serve to freeze the leaders in place while allowing him to mobilize capital and catch up.\n\n---\n\n### 
2. The Hardware Foundation: Jensen Huang and Nvidia\n*(The Strategy: Commoditizing the Software and Maximizing Volume)*\n\nNvidia sits in an entirely different position within the value chain. It does not sell software services directly to consumers; it sells the compute infrastructure (GPUs, networking, and software frameworks) that makes modern AI possible.\n\n#### 
A. The Classic Tech Play: "Commoditize Your Complement"\nIn business strategy, if your product relies on another product, you want that other product to be as cheap and widely available as possible so that all value accrues to your bottleneck.\n* **Nvidia’s bottleneck:** High-bandwidth memory, advanced packaging (TSMC’s CoWoS), and the proprietary CUDA software platform.\n* **Nvidia’s risk:** If OpenAI, Microsoft, and Google become the *only* three buyers of frontier AI compute, they gain massive monopsony power (buyer power). They could demand discounts or collectively transition to custom, in-house silicon (such as Google’s TPUs, Microsoft’s Maia, or Amazon’s Trainium).\n* **The Hugging Face Play:** By partnering with Hugging Face (the global clearinghouse for open-source AI models and datasets) and integrating **Nvidia DGX Cloud** directly into it, Jensen Huang ensures that:\n    
1. Tens of thousands of companies and independent developers build their own AI models instead of solely paying an API toll to OpenAI or Anthropic.\n    
2. The demand for Nvidia hardware remains broad-based, decentralized, and diverse, preventing proprietary labs from dictating terms to Nvidia.\n\n#### 
B. The Compute Math of Open Source\nContrary to intuitive belief, open-source AI does not decrease hardware demand; **it multiplies it**.\n* If one closed company serves 100 million users via an API, their infrastructure is hyper-optimized for efficiency.\n* If 10,000 separate companies download an open-source model from Hugging Face and train, fine-tune, and host it on their own servers, they require vastly more aggregate compute to achieve the same collective outcome. Nvidia sells more GPUs in an open-source, fragmented ecosystem than in a consolidated monopoly.\n\n#### 
C. Cementing the CUDA Lock-in\nBy linking DGX Cloud to Hugging Face, Nvidia provides developers with "one-click" optimization for Nvidia chips. Developers get used to Nvidia-specific libraries (TensorRT-LLM, Triton). Once millions of developers build workflows deeply reliant on this ecosystem, it becomes nearly impossible for competitors like AMD, Intel, or foreign chipmakers to displace Nvidia.\n\n---\n\n### 
3. The Geopolitical Dimension: The US State View\n*(National Security and Global Hegemony)*\n\nWhile corporate leaders push their respective commercial interests, the United States government views this landscape through the lens of strategic dominance over rivals, primarily China.\n\n	
1. **Strategic Leverage via Compute:** The U.S. Department of Commerce (via the Bureau of Industry and Security) does not restrict AI algorithms; it restricts **compute hardware**. Advanced models are difficult to intercept; shipping containers of physical, advanced semiconductors are easy to control.\n
2. **Export Control Alignment:** The U.S. government restricts Nvidia from selling its premier hardware (A100, H100, B200) to China. Jensen Huang, naturally, opposes broad export restrictions because it closes off a massive market (China historically represented 20-25% of Nvidia’s data center revenue). Supporting Hugging Face allows Nvidia to maximize its footprint everywhere else in the world.\n
3. **The Soft Power of Open Source:** When open-source models (hosted on platforms like Hugging Face, trained with Western values, architectures, and English-dominant datasets) become the global standard in Europe, Southeast Asia, and Latin America, the United States retains structural dominance over the world\'s digital infrastructure.

"""
}

final_state = workflow.invoke(init_state)

print(final_state)