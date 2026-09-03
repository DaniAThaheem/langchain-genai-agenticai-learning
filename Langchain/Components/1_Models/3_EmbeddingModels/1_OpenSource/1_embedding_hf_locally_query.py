from langchain_huggingface import HuggingFaceEmbeddings
import os
import sys

# Use a raw string for Windows paths to avoid escape-sequence warnings
os.environ["HF_HOME"] = r"D:\HF_Cache\embedding_model"
# Reduce tokenizer parallelism which can spike memory in some environments
os.environ["TOKENIZERS_PARALLELISM"] = "false"

try:
	embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
	vector = embeddings.embed_query("Doing my work")
	print(str(vector))
except MemoryError as e:
	print("MemoryError while loading the model:", e, file=sys.stderr)
	print(
		"Suggestions: run 64-bit Python, increase pagefile/close other apps, or use a smaller model",
		file=sys.stderr,
	)
except Exception as e:
	# Catch other native errors (e.g. OOMs coming from native libraries)
	print("Error while creating embeddings:", repr(e), file=sys.stderr)
	print(
		"If this is an out-of-memory issue try: 1) a smaller model like 'sentence-transformers/paraphrase-MiniLM-L3-v2'",
		file=sys.stderr,
	)
	raise