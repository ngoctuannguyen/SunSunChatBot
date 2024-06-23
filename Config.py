#Chunksize Data
chunk_size = 2000
chunk_overlap = 100
#Embeddings
MODEL_RETRIEVAL = "BAAI/bge-m3"
MODEL_RERANKERS = "BAAI/bge-reranker-base"
#BM25
BM25_K = 20
#Hybrid Search
Hybrid_Weight = [0.5, 0.5]
#Rerankers
ReRankers_K = 5
#Openai
GPT_Model = "gpt-3.5-turbo-0125"
Temperature = 0.5
Max_Tokens = 512