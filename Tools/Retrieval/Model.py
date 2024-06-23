import torch
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

class Embeddings:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Set device to cuda if available
    def Embeddings(self):
        Embeddings = HuggingFaceBgeEmbeddings(
            model_name="BAAI/bge-m3",  # Model name
            model_kwargs={"trust_remote_code": True, 'device': self.device},  # Set device to cuda if available and trust remote code
            encode_kwargs={"normalize_embeddings": True},  # Normalize embeddings
        )
        return Embeddings
    def Rerankers(self):
        Rerankers = HuggingFaceCrossEncoder(
            model_name="BAAI/bge-reranker-base",  # Model name
            model_kwargs={"trust_remote_code": True, 'device': self.device},  # Set device to cuda if available and trust remote code
        )
        return Rerankers
    def Chroma(self):
        Chroma = Chroma(persist_directory="MQICT",
                        embedding_function=self.Embeddings
                        )
        return Chroma
