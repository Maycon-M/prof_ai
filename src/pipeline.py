from src.pdf_processor import PDFProcessor
from src.vector_database import VectorDatabase
from src.document import Document
from typing import List
from sentence_transformers import SentenceTransformer
from transformers import pipeline as hf_pipeline
import configparser
import os
import requests

# Embeddings via Google Generative Language API
class GoogleEmbedder:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        # endpoint para text embeddings (v1)
        self.url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:embedText?key={self.api_key}"

    def encode(self, texts: list) -> list:
        instances = [{"text": t} for t in texts]
        response = requests.post(self.url, json={"instances": instances})
        response.raise_for_status()
        preds = response.json().get("predictions", [])
        return [item.get("embedding") for item in preds]

class Pipeline:
    def __init__(self, pdf_path: str, db_path: str = "./chroma_db", collection_name: str = "pdf_collection", model_name: str = "all-mpnet-base-v2"):
        self.pdf_path = pdf_path
        self.pdf_processor = PDFProcessor(pdf_path)
        self.vector_db = VectorDatabase(path=db_path)
        self.collection_name = collection_name
        # escolher embedder: Google ou local
        if model_name.lower() == "google":
            cfg = configparser.ConfigParser()
            cfg.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
            api_key = cfg['DEFAULT']['GOOGLE_API_KEY']
            google_model = cfg['DEFAULT']['MODEL']
            self.embedder = GoogleEmbedder(api_key, google_model)
        else:
            # embedder local SBERT
            self.embedder = SentenceTransformer(model_name)
        # modelo de QA extractivo
        self.qa_pipeline = hf_pipeline(
            "question-answering",
            model="deepset/roberta-base-squad2",
            tokenizer="deepset/roberta-base-squad2"
        )

    def initialize_collection(self, create_new: bool = False):
        if create_new:
            self.vector_db.create_collection(self.collection_name)
        else:
            self.vector_db.get_or_create_collection(self.collection_name)

    def run(self):
        # ensure the collection is initialized before adding documents
        self.initialize_collection()
        print(f"Processing PDF: {self.pdf_path}")
        text = self.pdf_processor.extract_text()
        chunks = self.pdf_processor.chunk_text(text)

        documents_to_add = []
        for i, chunk in enumerate(chunks):
            # gerar embedding (GoogleEmbedder ou SBERT)
            if isinstance(self.embedder, GoogleEmbedder):
                embedding = self.embedder.encode([chunk])[0]
            else:
                embedding = self.embedder.encode(chunk).tolist()
            doc = Document(text=chunk, embedding=embedding, metadata={"chunk_id": i})
            documents_to_add.append(doc)
        
        print(f"Adding {len(documents_to_add)} documents to vector database.")
        self.vector_db.add_documents(documents_to_add)
        print("PDF processing and storage complete.")

    def query_documents(self, query_text: str, n_results: int = 2):
        # ensure the collection is initialized before querying
        self.initialize_collection()
        # vetor da query
        # vetor da query
        if isinstance(self.embedder, GoogleEmbedder):
            query_embedding = self.embedder.encode([query_text])[0]
        else:
            query_embedding = self.embedder.encode(query_text).tolist()
        # busca vetorial top-k
        results = self.vector_db.query(query_embeddings=[query_embedding], n_results=n_results)
        # monta contexto com os trechos retornados
        docs = results.get("documents", [[]])[0]
        if not docs:
            # sem documentos, não roda QA
            results["answer"] = None
            results["answer_score"] = None
            return results
        context = "\n\n".join(docs)
        # extrai resposta com modelo de QA
        answer = self.qa_pipeline(question=query_text, context=context)
        # anexa resposta e score ao resultado
        results["answer"] = answer.get("answer")
        results["answer_score"] = answer.get("score")
        return results


