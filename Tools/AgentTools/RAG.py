import os
import json
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma

load_dotenv()

from langchain.tools.retriever import create_retriever_tool
from langchain_openai import OpenAIEmbeddings

# Load the OpenAI API key from environment variables
embed_models = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize the Chroma vector store with the embedding function and persistence directory
VectorStoreDB = Chroma(embedding_function=embed_models,
                       persist_directory="SunVectorDB",)

# Create a retriever from the vector store
VectorStore = VectorStoreDB.as_retriever(
    search_type="mmr",  # Also test "similarity"
    search_kwargs={"k": 3}
)

# Define the MyRAGTool using the create_retriever_tool function
MyRAGTool = create_retriever_tool(
    retriever=VectorStore,
    name="SunInfoRetrievalTool",  # Adjusted for compatibility
    description="Retrieve information related to Sun* company."
)