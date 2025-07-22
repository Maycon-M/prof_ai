import chromadb
from typing import List, Dict, Any
from src.document import Document

class VectorDatabase:
    def __init__(self, path: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = None

    def get_collection(self, collection_name: str):
        self.collection = self.client.get_collection(name=collection_name)

    def create_collection(self, collection_name: str):
        self.collection = self.client.create_collection(name=collection_name)

    def get_or_create_collection(self, collection_name: str):
        try:
            self.collection = self.client.get_collection(name=collection_name)
        except:
            self.collection = self.client.create_collection(name=collection_name)

    def delete_collection(self, collection_name: str):
        self.client.delete_collection(name=collection_name)

    def add_documents(self, documents: List[Document]):
        if not self.collection:
            raise ValueError("Collection not initialized. Call get_or_create_collection or create_collection first.")

        ids = [f"doc_{i}" for i in range(len(documents))]
        embeddings = [doc.embedding for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        documents_content = [doc.text for doc in documents]

        self.collection.add(
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents_content,
            ids=ids
        )

    def query(self, query_embeddings: List[List[float]], n_results: int = 2) -> Dict[str, Any]:
        if not self.collection:
            raise ValueError("Collection not initialized. Call get_or_create_collection or get_collection first.")
        
        results = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results
        )
        return results


