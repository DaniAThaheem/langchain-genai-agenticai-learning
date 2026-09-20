# LangChain · GenAI · Agentic AI — Learning Repository

A hands-on, component-by-component walkthrough of the LangChain framework, built while learning it from first principles. Every folder isolates one concept, and most concepts are written twice: once as the **problem** (the painful manual way) and once as the **solution** (the LangChain way). The goal was to understand *why* each abstraction exists, not just how to call it.

**Primary LLM:** Google Gemini (`gemini-flash-latest`) via `langchain-google-genai`
**Secondary:** Hugging Face — both remote (`HuggingFaceEndpoint`) and local (`HuggingFacePipeline`) with `meta-llama/Llama-3.1-8B-Instruct`
**Embeddings:** `gemini-embedding-2` and `sentence-transformers/all-MiniLM-L6-v2`
**Vector stores:** Chroma (persistent) and FAISS (in-memory)

---

## Repository Structure

```
Langchain/Components/
├── 1_Models/                      # LLMs, chat models, embedding models
├── 2_Prompts/                     # Prompt templates, messages, chat history
├── 3_Chains/                      # LCEL, Runnables, chain topologies
├── 4_RAG/                         # Loaders, splitters, vector stores, retrievers
├── 6_Agents/                      # Tools, tool calling, toolkits, ReAct agent
└── Extra_1_Structured_Output/     # Structured output + output parsers
```

---

## 1 · Models

| Path | What it covers |
|---|---|
| `2_ChatModels/2_CloseSource/1_chatmodel_google.py` | Closed-source chat model via `ChatGoogleGenerativeAI` |
| `2_ChatModels/1_OpenSource/1_chatmodel_hf_interface.py` | Open-source model served remotely through `HuggingFaceEndpoint` + `ChatHuggingFace` |
| `2_ChatModels/1_OpenSource/2_chatmodel_hf_locally.py` | Same model pulled and run locally via `HuggingFacePipeline`, with a custom `HF_HOME` cache |
| `3_EmbeddingModels/` | `embed_query` vs `embed_documents`, for both Google and local MiniLM |
| `project/document_similarity_app_without_rag.py` | Mini project — embed a document set, embed a query, rank with `cosine_similarity`, pass the top hit back to the LLM as context |

The similarity project is deliberately labelled *without RAG*: it is the manual version of retrieval, built before the RAG section so the vector-store machinery later has something to be compared against.

## 2 · Prompts

- `Messages/problem_understanding.py` — the failure case: chat is stateless, so history is kept in a bare list and the model loses track of who said what.
- `Messages/static_message_solution.py` — the fix: typed `SystemMessage` / `HumanMessage` / `AIMessage` in a running loop.
- `Messages/dynamic_message_solution.py` — `ChatPromptTemplate` with runtime variables (`{domain}`, `{topic}`).
- `Messages/message_placeholder.py` — `MessagesPlaceholder` to inject a persisted conversation into a template.
- `Prompts/static_prompt.py` / `dynamic_prompt.py` — a Streamlit "Research Summarizer" UI, first with a raw text box, then with a parameterised `PromptTemplate` (paper / style / length).
- `Prompts/Properties/prompt_generator.py` — serialising a template with `template.save()` for reuse via `load_prompt()`.

## 3 · Chains

**Runnable_Concepts_Jupyter_Notebook/** is the conceptual core of the repo. Two notebooks rebuild LangChain's own design:

1. `problem_that_leads_to_runnables.ipynb` — mock `LLM.predict()` and `PromptTemplate.format()` classes. Because the interfaces differ, every new combination needs a bespoke `LLMChain` class. This is the combinatorial explosion that motivated LCEL.
2. `raw_runnable_implementation.ipynb` — introduce an abstract `Runnable` base class with a single `invoke()` method, then a `RunnableConnector` that chains any list of runnables — and, because the connector is itself a runnable, chains of chains work for free.

Having reinvented it, the framework versions follow:

| File | Concept |
|---|---|
| `LCEL/lang_chain_expression_language.py` | The pipe operator: `template \| model \| parser` |
| `Runnable_Types/runnable_sequence.py` | Explicit `RunnableSequence` |
| `Runnable_Types/runnable_parallel.py` | Fan-out — one topic → tweet and LinkedIn post simultaneously |
| `Runnable_Types/runnable_passthrough.py` | Carrying an intermediate value forward unchanged |
| `Runnable_Types/runnable_lambda.py` | Arbitrary Python in a chain (word count alongside the LLM output) |
| `Runnable_Types/runnable_branch.py` | Conditional routing |
| `Chain_Types/simple_chain.py` | Sequential — identify process, then report on it |
| `Chain_Types/parallel_chain.py` | Two analyses run in parallel, then merged by a third LLM call |
| `Chain_Types/conditional_chain.py` | Classifier → `RunnableBranch` → sentiment-specific response, with a `RunnableLambda` fallback |

`conditional_chain.py` is the most complete pattern here: a Pydantic-parsed classifier feeds a branch that dispatches to different prompts based on the parsed field.

## 4 · RAG

**Document loaders** — `TextLoader`-style manual `Document` construction, `PyPDFLoader`, `CSVLoader`, `DirectoryLoader`, `WebBaseLoader`, plus an explicit `load()` vs `lazy_load()` comparison showing eager vs on-demand memory behaviour.

**Text splitters** — all four strategies, in increasing sophistication:
- Length-based (`CharacterTextSplitter`) on raw text and on loaded PDF documents
- Text-structure-based (`RecursiveCharacterTextSplitter`)
- Document-structure-based (`from_language` with `Language.PYTHON` and `Language.MARKDOWN`)
- Semantic (`SemanticChunker` with a standard-deviation breakpoint threshold)

**Vector stores** — `chromadb_vector_store_demo.py` is a full interactive CRUD menu over a persistent Chroma collection: add documents, dump embeddings and metadata, similarity search, similarity search *with scores*, update a document by ID, delete by ID.

**Retrievers** — four strategies compared on the same corpus:
| Retriever | Problem it solves |
|---|---|
| `vector_store_retriever.py` | Baseline similarity search as a retriever interface |
| `maximal_marginal_relevence_retriever.py` | Redundancy — MMR with `lambda_mult` to diversify near-duplicate hits |
| `multi_query_retriever.py` | Vague queries — the LLM rewrites one query into several |
| `contextual_compression_retriever.py` | Noisy chunks — `LLMChainExtractor` strips irrelevant passages out of retrieved documents |
| `wikipedia_retriever.py` | Retrieval from an external knowledge source (wrapped in error handling) |

The retriever corpus is intentionally adversarial: documents deliberately mix cricket-player text with media-player text so that MMR and contextual compression have something real to fix.

## 5 · Structured Output (`Extra_1_Structured_Output`)

Two distinct routes, correctly separated:

**`with_structured_output()`** — for models with native schema support. The same product review is parsed three ways:
- `Typed_Dict_Method/` — `TypedDict` + `Annotated` field descriptions
- `Pydantic_Method/` — `BaseModel` + `Field(description=...)`, with validation, `Optional`, and `Literal` constraints
- `Json_Schema_Method/` — a hand-written JSON Schema with `required`, `enum`, and nullable types

**Output parsers** — for models *without* native structured output. `String_Output_Parser/problem.py` shows the manual pain (invoke, pull `.content`, feed it into the next template, invoke again); `strOutputParser_solution.py` collapses all of it into one pipe. Then `JsonOutputParser` (structure, no schema enforcement) and `PydanticOutputParser` (schema enforced via `get_format_instructions()` injected as a partial variable).

## 6 · Agents

**Tool creation**, three ways with increasing control:
- `tools_decorator_method.py` — the `@tool` decorator; name, description, and args inferred from signature and docstring
- `structured_tool_method.py` — `StructuredTool.from_function` with an explicit Pydantic `args_schema`
- `base_tool_method.py` — subclassing `BaseTool` and implementing `_run`

**Built-in tools** — `DuckDuckGoSearchRun`, `ShellTool`.
**Toolkits** — `toolkit.py`, grouping related tools behind a `get_tools()` interface.

**Tool calling** — `tool_calling_demo.py` walks the full four-step loop explicitly: create → bind (`bind_tools`) → model emits `tool_calls` → execute the function → append a `ToolMessage` with the matching `tool_call_id` → re-invoke. `currency_converter.py` extends this to a **dependent** two-tool chain, where the output of `conversion_factor` has to be injected into the arguments of `converter` before it can run — which is exactly the hand-wiring an agent automates.

**Agent** — `search_agent.py` closes the loop: a ReAct agent (`create_react_agent` + `AgentExecutor`) with a custom weather tool and DuckDuckGo search, given a multi-hop question ("capital of Pakistan, and its current weather") that requires chaining two tools without being told the order.

---

## Setup

```bash
git clone https://github.com/DaniAThaheem/langchain-genai-agenticai-learning.git
cd langchain-genai-agenticai-learning

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r Langchain/Components/6_Agents/requirements.txt
```

Each component folder carries its own `requirements.txt`; the `6_Agents` one is a superset. Create a `.env` at the component root you are running:

```env
GOOGLE_API_KEY=your_key_here
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

Then run any example directly:

```bash
python Langchain/Components/3_Chains/LCEL/lang_chain_expression_language.py
streamlit run Langchain/Components/2_Prompts/Prompts/dynamic_prompt.py
```

---

## Concepts Covered

`LLMs` · `Chat models` · `Embedding models` · `Open vs closed source providers` · `Local vs hosted inference` · `Prompt templates` · `Message types` · `Chat history` · `MessagesPlaceholder` · `LCEL` · `Runnables` · `Sequential / parallel / conditional chains` · `Structured output` · `Pydantic / TypedDict / JSON Schema` · `Output parsers` · `Document loaders` · `Text splitting strategies` · `Vector stores` · `Similarity search & scoring` · `Retrievers` · `MMR` · `Multi-query` · `Contextual compression` · `Tool creation & binding` · `Tool calling loop` · `Toolkits` · `ReAct agents`
