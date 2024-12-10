from enum import Enum
from typing import List, Optional

from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.llms import LLM
from llama_index.core.objects import ObjectRetriever
from llama_index.core.tools import BaseTool


class AgentMode(str, Enum):
    """Agent mode."""
    DEFAULT = "default"
    REACT = "react"
    FUNCTION_CALLING = "function_calling"

class AgentConfig(BaseModel):
    """Configuration for a single agent in the multi-agent system."""
    
    name: str
    description: str
    system_prompt: Optional[str] = None
    tools: Optional[List[BaseTool]] = None
    tool_retriever: Optional[ObjectRetriever] = None
    tools_requiring_human_confirmation: List[str] = Field(default_factory=list)
    can_handoff_to: List[str] = Field(default_factory=list)
    handoff_prompt_template: Optional[str] = None
    llm: Optional[LLM] = None
    is_root_agent: bool = False
    mode: AgentMode = AgentMode.DEFAULT
