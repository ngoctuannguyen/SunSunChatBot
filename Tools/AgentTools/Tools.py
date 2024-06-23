from enum import Enum
from typing import Optional
from typing_extensions import TypedDict

from langchain.pydantic_v1 import BaseModel, Field
from langchain_community.retrievers.wikipedia import WikipediaRetriever

class AvailableTools(str, Enum):
    ACTION_SERVER = "action_server_by_sema4ai"
    CONNERY = "ai_action_runner_by_connery"
    DDG_SEARCH = "ddg_search"
    TAVILY = "search_tavily"
    TAVILY_ANSWER = "search_tavily_answer"
    RETRIEVAL = "retrieval"
    ARXIV = "arxiv"
    YOU_SEARCH = "you_search"
    SEC_FILINGS = "sec_filings_kai_ai"
    PRESS_RELEASES = "press_releases_kai_ai"
    PUBMED = "pubmed"
    WIKIPEDIA = "wikipedia"
    DALL_E = "dall_e"
    
class ToolConfig(TypedDict):
    ...

class BaseTool(BaseModel):
    type: AvailableTools
    name: Optional[str]
    description: Optional[str]
    config: Optional[ToolConfig]
    multi_use: Optional[bool] = False

class ActionServerConfig(ToolConfig):
    url: str
    api_key: str

class DDGInput(BaseModel):
    query: str = Field(description="search query to look up")


class ArxivInput(BaseModel):
    query: str = Field(description="search query to look up")


class PythonREPLInput(BaseModel):
    query: str = Field(description="python command to run")


class DallEInput(BaseModel):
    query: str = Field(description="image description to generate image from")

class Wikipedia(BaseTool):
    type: AvailableTools = Field(AvailableTools.WIKIPEDIA, const=True)
    name: str = Field("Wikipedia", const=True)
    description: str = Field(
        "Searches [Wikipedia](https://pypi.org/project/wikipedia/).", const=True
    )
    
class ActionServer(BaseTool):
    type: AvailableTools = Field(AvailableTools.ACTION_SERVER, const=True)
    name: str = Field("Action Server by Sema4.ai", const=True)
    description: str = Field(
        (
            "Run AI actions with "
            "[Sema4.ai Action Server](https://github.com/Sema4AI/actions)."
        ),
        const=True,
    )
    config: ActionServerConfig
    multi_use: bool = Field(True, const=True)