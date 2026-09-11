from langchain_community.document_loaders import CSVLoader
from pathlib import Path


file_path = Path(__file__).parent / "Sample" / "sample_csv_data.csv"

loader = CSVLoader(file_path=file_path)

docs = loader.lazy_load()

for doc in docs:
    print(doc.metadata)
    print(doc.page_content)