import os
import shutil
import hashlib
from uuid import uuid4
from typing import List
from dotenv import load_dotenv
load_dotenv()
# Backend FastAPI Libraries
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# Langchain Libraries
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

embed_models = OpenAIEmbeddings(show_progress_bar=True)

class VectorDatabase:
    """
    VectorDatabase class to store and manage vectors
    """
    def __init__(self):
        self.vectordb = Chroma(
            embedding_function=embed_models,
            persist_directory="Test",
        )

    def add_documents(self, docs: List[str]):
        self.vectordb.add_documents(docs)

    def delete_database(self):
        shutil.rmtree(self.vectordb._persist_directory)  # Accessing the private attribute _persist_directory
        os.makedirs(self.vectordb._persist_directory)

# FastAPI Application setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this if you want to limit origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_session_id(request: Request, call_next):
    """Middleware to add a session ID to each request."""
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = hashlib.md5(str(uuid4()).encode()).hexdigest()
    request.state.session_id = session_id
    response = await call_next(request)
    response.set_cookie(key="session_id", value=session_id)
    return response

vector_db = VectorDatabase()

@app.post("/add_data/")
async def add_data(files: List[UploadFile] = File(...)):
    docs = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    for file in files:
        temp_file_path = f"./data/{file.filename}"
        print(os.path.join(temp_file_path)) 
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())
        raw_content = PyPDFLoader(temp_file_path)
        content = raw_content.load()
        content_chunks = text_splitter.split_documents(content)
        for chunk in content_chunks:
            if isinstance(chunk, bytes):
                chunk = chunk.decode('utf-8')
            docs.append(chunk)
        os.remove(temp_file_path)  # Clean up the temp file
    print(docs)
    vector_db.add_documents(docs)
    return {"status": "Documents added successfully"}

@app.post("/delete_database/")
async def delete_database():
    vector_db.delete_database()
    return {"status": "Database deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("API:app", host="127.0.0.1", port=11100, reload=True)
