from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel


load_dotenv()

model1 = ChatGoogleGenerativeAI(model="gemini-flash-latest")

parser = StrOutputParser()

prompt1 = PromptTemplate(
    template="Evaluate my current academic history based on {data} and evaluate the current status and alignment with the give scholorship requirements. Future road map for next few months becuase the current month and year is {month}. List the cousrses to do, the research to read and what to do for maximizing the chances for a Pakistani student. Also explain the efforts required to meet the reqirements",
    input_variables=["data", "month"]
)

prompt2 = PromptTemplate(
    template="Evaluate the current given data {data} and list the required documents and how to get them for prepared for the given scholarship as the current month is {month}",
    input_variables=["data", "month"]
)

prompt3 = PromptTemplate(
    template="Merge the given evaluation, roadmap and document requirement and prepare a detailed report with logical flow, clearly communicated "
)

parallel_chains = RunnableParallel(
    {
        "evaluation_and_roadmap": prompt1 | model1 | parser,
        "requirements_identification": prompt2 | model1 | parser
    }
)


merge_chain = prompt3 | model1 | parser


final_chain = parallel_chains | merge_chain

result = final_chain.invoke(
    {
        "data" : """
Executive Summary
The Erasmus Mundus Joint Master Degree (EMJMD) in Artificial Intelligence represents one of the most prestigious fully funded graduate opportunities globally. Funded by the European Commission, these programs offer tuition coverage, travel allowances, and a monthly living stipend (typically ~€1,400/month) across a multi-country mobility framework. 

Because selection is decentralized and run directly by university consortia (e.g., EMAI, JEMARO, BDMA), acceptance rates are typically below 5–8%. Winning an award requires not only technical mastery in core computing disciplines, but also demonstrated adaptability to transnational academic mobility.

1. End-to-End Application Lifecycle
[Phase 1: Oct–Nov]        [Phase 2: Dec–Jan]         [Phase 3: Feb–Mar]       [Phase 4: Apr–Aug]
Program Selection    ➜    Dossier Assembly     ➜     Technical Audits    ➜    Outcomes & Visa
& Track Mapping           & Submission               & Interviews             Processing

1. Program & Mobility Track Selection: Filter the official EMJMD Catalogue for specialized curricula (Computer Vision, Robotics, NLP, Data Governance). Candidates study in at least two different European partner institutions.
2. Eligibility & Profile Audit: Ensure alignment with minimum requirements: 180 ECTS Bachelor’s degree in STEM, verifiable proficiency in foundational mathematics, and accredited English proficiency (IELTS 6.5–7.0+ or TOEFL 90–100+).
3. Application Dossier Preparation: Assemble targeted materials: 
Europass-formatted CV
Letters of recommendation (LoRs)
Notarized/translated transcripts
Bespoke Statement of Purpose (SoP).
4. Direct Consortium Submission: 
Submit dossiers directly to 2–3 selected consortia portals between October and mid-February, verifying the scholarship selection checkbox is marked.
5. Evaluation & Interviews:
 Shortlisted applicants undergo technical evaluations and video interviews assessing 
mathematical foundations, 
research methodologies, 
cultural readiness.
6. Consortium Finalization: 
Notification of status (Main List, Reserve List, or Non-selected) occurs between March and May, followed by visa logistics for the entry country.

2. Key Strategies to Maximize Selection Probability

Academic excellence is the baseline; selection committees prioritize candidates who show 
Verified research potential
Clear institutional alignment
Cross-cultural adaptability.

 A. Provide Concrete Technical Proof (Show, Don’t Tell)
Open-Source & Code Repositories:
 Embed clickable hyperlinks in your CV to clean, documented GitHub repositories, interactive demos (e.g., Hugging Face Spaces), or Kaggle notebooks showing implemented machine learning models.
Highlight Foundational Mathematics:
 Consortia heavily weigh performance in Linear Algebra, Vector Calculus, and Probability. Ensure your transcripts explicitly reflect these coursework titles or supplement them with accredited certifications.
Undergraduate Research & Publications:
 Even non-peer-reviewed pre-prints (arXiv), technical blog posts, or high-scoring capstone theses significantly elevate candidates above those with only industry or coursework experience.

B. Map a Cohesive Consortium Trajectory
Curriculum-Specific Alignment:
Generic essays lead to immediate rejection. Explicitly detail why you chose 
Track A at University X** followed by **Track B at University Y**, naming specific laboratories, professors, or ongoing EU-funded research projects.
Clear Post-Degree Vision: 
Clearly state whether your trajectory leads to an applied industrial R&D role or a PhD, and explain how this specific joint degree serves as the bridge.

C. Demonstrate Cross-Cultural Agility
EMJMD dropouts and underperformance are frequently caused by culture shock and the stress of relocating every 6–12 months.
Use your Statement of Purpose to highlight prior international exposure, remote work in distributed teams, multi-lingual skills, or experience operating outside your comfort zone.

D. Secure Context-Specific Letters of Recommendation
Select academic references who can speak directly to your **quantitative logic, programming independence, and research capacity**. 
Avoid generic praise; recommenders should reference specific projects, challenges you solved, and your relative standing (e.g., *"ranked in the top 5percent of students in Advanced Algorithms"*).

E. Prepare for the Technical Interview
* Treat the interview as a dual defense of your CV and a rapid-fire oral exam.
Expect technical questions on core ML theory (e.g., gradient descent mechanics, regularizations, transformer architectures, bias-variance tradeoff) along with questions addressing how you will navigate living across multiple European nations.


My Current Work
Academic foundation
Matric: 897 marks (BISE Multan, 2020); FSc Pre-Engineering: 978/1100
BSIT from BZU Multan, 2026 — CGPA 3.83/4.00, class topper
96th percentile (top 4% nationally) on the HEC National Skill Competency Test 2026
Technical base going in
Full-stack: MERN, Flutter/Dart/GetX, SQL/NoSQL databases
Python: Pandas, NumPy, Matplotlib, Seaborn
FYP: an AI agent pipeline (Gemini-based) for a Flutter app — real applied AI experience, not just coursework
AI-specific learning currently underway
Actively learning LangChain and agent-building (primary focus), with CS50's AI with Python running as a secondary track
Studied concepts in n8n, Pipecat, and LiveKit for voice agents, but no hands-on project yet
Tracking this in a GitHub repo with modular examples (LLMs, chat models, embeddings — open and closed source)
Most recent hands-on work: open-source embedding models via Hugging Face, plus a document-similarity app using Google GenAI embeddings and a few chat model integrations (Gemini, local/remote Llama via Hugging Face)
Gaps relative to a Masters in AI
No formal ML/DL coursework yet (no linear algebra/stats-for-ML, no deep learning theory, no published or graded ML projects)
No voice-agent project completed end-to-end (LiveKit/Pipecat still conceptual, not built)
No research or thesis-style AI work — FYP used AI as a tool, not as the subject of study


My Current Documents
CNIC
Passport
Result Cards
Transcripts

""",
        "month":"September 2026"
    }
)

print(result)