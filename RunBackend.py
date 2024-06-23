import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from Utils.Prompt.Prompt import BINGSEARCH_PROMPT
from Tools.AgentTools.BingSearch import MyBingSearch

from typing import Any, Dict, Mapping, Optional, Sequence, Union

from dotenv import load_dotenv
load_dotenv()


llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    temperature=0.7,
    max_tokens=512,
)

vectorstore = Chroma(embedding_function=OpenAIEmbeddings(),
                    persist_directory="Test", )

RETRIEVAL_DESCRIPTION = """Can be used to look up information that was uploaded to this assistant.
If the user is referencing particular files, that is often a good hint that information may be here.
If the user asks a vague question, they are likely meaning to look up info from this retriever, and you should call it!"""

def get_retriever():
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

def get_retrieval_tool():
    return create_retriever_tool(
        get_retriever(),
        "Retriever",
        RETRIEVAL_DESCRIPTION,
    )
    
retrieval = get_retrieval_tool()

tools = [
    MyBingSearch(k=5),
    retrieval
]

agent = create_openai_tools_agent(llm, tools, BINGSEARCH_PROMPT)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, return_intermediate_steps=True)

def GenerateAnswer(question: str) -> Dict:
    result = agent_executor.invoke({"question": question})
    # Convert result to dictionary or other serializable format
    return result

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/")
async def query_handler(request: Request, query: QueryRequest):
    """API endpoint to process a question and return the answer."""
    answer = GenerateAnswer(query.question)
    json_compatible_answer = jsonable_encoder(answer)
    return JSONResponse(content={"text": json_compatible_answer})

if __name__ == "__main__":
    uvicorn.run("RunBackend:app", host="127.0.0.1", port=11101, reload=True)
