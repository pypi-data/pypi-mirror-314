from typing import Any, Optional

from llama_index.core.tools import AsyncBaseTool, ToolSelection
from llama_index.core.llms import ChatMessage
from llama_index.core.workflow import Event

class ToolApprovalNeeded(Event):
    """Emitted when a tool call needs approval."""
    id: str
    tool_name: str
    tool_kwargs: dict

class ApproveTool(Event):
    """Required to approve a tool."""
    id: str
    tool_name: str
    tool_kwargs: dict
    approved: bool
    reason: Optional[str] = None

class LLMInput(Event):
    """LLM input."""
    input: list[ChatMessage]
    current_agent: str

class AgentSetup(Event):
    """Agent setup."""
    input: list[ChatMessage]
    tools: list[AsyncBaseTool]

class LLMOutput(Event):
    """LLM output."""
    delta: str
    response: str
    tool_calls: list[ToolSelection]
    raw_response: Any

class ToolCall(Event):
    """All tool calls are surfaced."""
    tool_name: str
    tool_kwargs: dict
    tool_output: Any

class HandoffEvent(Event):
    """Internal event for agent handoffs."""
    from_agent: str
    to_agent: str
    reason: str
