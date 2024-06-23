from langchain_experimental.text_splitter import SemanticChunker
from Tools.Retrieval.Model import Embeddings

class SemanticChunker:
    def __init__(self):
        self.Embeddings = Embeddings().Embeddings()
        self.Chunker = SemanticChunker(self.Embeddings,breakpoint_threshold_type="percentile")
    def chunk(self,Data):
        chunks = self.Chunker.split_documents(Data)
        return chunks