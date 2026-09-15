from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


class Retriever:
    def __init__(self, vector_store_path: str):
        self.vector_store_path = Path(vector_store_path)

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vectordb = Chroma(
            persist_directory=str(self.vector_store_path),
            embedding_function=self.embedding_model
        )

    def retrieve(self, question: str, k: int = 2):
        return self.vectordb.similarity_search(
            question,
            k=k
        )