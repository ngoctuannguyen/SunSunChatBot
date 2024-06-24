import os
import json
import torch
import pickle
import Config
import hashlib
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import LLMChain
from langchain import PromptTemplate
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage, AIMessage
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
# from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
from multiprocessing.pool import ThreadPool
import uvicorn

load_dotenv()

embed_models = OpenAIEmbeddings(show_progress_bar=True)
VectorStore = Chroma(embedding_function=embed_models,
                    persist_directory="./Test")
VectorStore.as_retriever(search_kwargs={"k": 5})

llm = ChatOpenAI(
    model=Config.GPT_Model,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    temperature=Config.Temperature,
    max_tokens=Config.Max_Tokens,
)

def process_question_with_rag(question):
    """Process a question using RAG (Retrieval-Augmented Generation) and update the memory."""
    # Define the prompt template for generating the final response
    prompt_template = """
        You are Sunsun, a powerful AI created by NguyenTuanNgoc.
        You have advanced coding and algorithmic skills, and you can search for real-time information on Google.
        This is some context can related to the question:
        {context}
        Question: {question}
        If the content is not enough information, let answer with your knowledge.
        Let answer by Vietnamese:
        Answer:
    """.strip()
    
    PROMPT = PromptTemplate.from_template(template=prompt_template)
    
    # Define the prompt template for generating a standalone question
    condense_question_prompt_template = """
    Dưới đây là một câu hỏi và lịch sử câu trả lời cho câu hỏi gần nhất, bạn hãy từ lịch sử và câu hỏi để tạo ra câu hỏi phù hợp nhất với ngữ cảnh, nếu không có lịch sử trò chuyện bạn chỉ cần làm rõ câu hỏi thôi nhé.    Chat History:
    {chat_history}
    Follow Up Input: {question}
    """
    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(condense_question_prompt_template)
    
    # Create a chain for generating standalone questions
    question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT, verbose=True)
    
    # Create a chain for generating the final response
    doc_chain = load_qa_chain(
        llm=llm,
        chain_type='stuff',
        prompt=PROMPT,
        verbose=True,
    )
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        input_key='question',
        output_key='answer',
        memory_key='chat_history',
        return_messages=True,
    )
    # Combine retrievers and chains into a Conversational Retrieval Chain
    chain = ConversationalRetrievalChain(
        retriever=VectorStore.as_retriever(search_kwargs={"k": 5}),
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
        return_source_documents=True,
        memory=memory,
        verbose=True,
        get_chat_history=lambda h: h
    )

    # Process the question and get the response
    response = chain({"question": question})

    # Update memory after responding
    return response['answer']

# FastAPI Application setup
app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/")
async def query_handler(query: QueryRequest):
    """API endpoint to process a question and return the answer."""
    answer = process_question_with_rag(query.question)
    return JSONResponse(content={"text": answer})

if __name__ == "__main__":
    uvicorn.run("RAG:app", host="127.0.0.1", port=7077, reload=True)
