import torch

from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

class VectorDatabase:
    """
    VectorDatabase class to store and add vectors"""
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name="BAAI/bge-m3",
            model_kwargs={"trust_remote_code": True, 'device': self.device},
            encode_kwargs = {"normalize_embeddings": True}, )
        self.vectordb = Chroma(
            embedding=self.embeddings,
            collection_name="MQICT",
            persist_directory="MQICT",
        )
    def add_documents(self, docs):
        self.vectordb.add_documents(docs)
        
        