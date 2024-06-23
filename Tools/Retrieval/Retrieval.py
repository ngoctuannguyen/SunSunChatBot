from langchain_community.vectorstores import Qdrant
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from Tools.Retrieval.Model import Embeddings
import torch
class Retrieval:
    """
    Class for retrieval of documents with BM25Retriever and EnsembleRetriever finally reranked with CrossEncoderReranker.
    """
    def __init__(self, Data):
        self.Data = Data  # Data
        self.top_k_retrieval = 20  # Top k retrieval
        self.top_k_reranker = 5
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Set device to cuda if available
        self.Embeddings = Embeddings().Embeddings()
        self.Rerankers = Embeddings().Rerankers()
        self.Chroma = Embeddings().Chroma()
        self.BM25_Retriever = BM25Retriever.from_texts(
            [doc.page_content for doc in self.Data],  # Get content from Data
            metadatas=[doc.metadata for doc in self.Data]  # Get metadata from Data
        )
        self.BM25_Retriever.k = self.top_k_retrieval
        self.Chroma.k = self.top_k_retrieval

    def search(self, query):
        ensemble_retriever = EnsembleRetriever(retrievers=[self.BM25_Retriever, self.Chroma], weights=[0.5, 0.5])
        compressor = CrossEncoderReranker(model=self.Rerankers, top_n=self.top_k_reranker)
        hybrid_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=ensemble_retriever)
        return hybrid_retriever.search(query)

# Query = "What is the capital of India?"
# Data = Data  # Load the documents
# Retrieval = Retrieval(Data)
# Results = Retrieval.search(Query)
