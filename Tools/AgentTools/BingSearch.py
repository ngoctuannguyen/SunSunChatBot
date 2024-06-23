
import asyncio
from typing import Dict, List, Optional, Type

from concurrent.futures import ThreadPoolExecutor
from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from langchain_community.utilities import BingSearchAPIWrapper
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain.chains import LLMChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationalRetrievalChain

from dotenv import load_dotenv
load_dotenv()

class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")

class MyBingSearch(BaseTool):
    """Tool for a Bing Search Wrapper"""
    
    name = "Searcher"
    description = "Thực hiện tìm kiếm thông tin trên internet nếu như câu hỏi không hỏi về công ty Sun*.\n"
    args_schema: Type[BaseModel] = SearchInput

    k: int = 5
    
    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        bing = BingSearchAPIWrapper(k=self.k)
        return bing.results(query,num_results=self.k)
            
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        bing = BingSearchAPIWrapper(k=self.k)
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(ThreadPoolExecutor(), bing.results, query, self.k)
        return results