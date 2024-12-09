from typing import Any, Dict, List, Optional, Union

from llama_index.core.agent.multi_agent.agent_config import AgentConfig
from llama_index.core.agent.multi_agent.workflow_events import HandoffEvent, ToolCall, LLMInput, LLMOutput
from llama_index.core.llms import ChatMessage, LLM
from llama_index.core.memory import BaseMemory, ChatMemoryBuffer
from llama_index.core.prompts import BasePromptTemplate, PromptTemplate
from llama_index.core.tools import BaseTool, AsyncBaseTool, FunctionTool, adapt_to_async_tool
from llama_index.core.workflow import Context, StartEvent, StopEvent, Workflow, step
from llama_index.core.settings import Settings


DEFAULT_HANDOFF_PROMPT = """Useful for handing off to another agent. 
If you are currently not equipped to handle the user's request, please hand off to the appropriate agent.

Currently available agents:
{agent_info}
"""

DEFAULT_STATE_PROMPT = """Here is the current system state:
{state}
"""


async def handoff(to_agent: str, reason: str) -> HandoffEvent:
    """Handoff to the given agent."""
    return f"Handed off to {to_agent}"


class MultiAgentSystem(Workflow):
    """A workflow for managing multiple agents with handoffs."""
    
    def __init__(
        self,
        agent_configs: List[AgentConfig],
        initial_state: Optional[Dict] = None,
        memory: Optional[BaseMemory] = None,
        handoff_prompt: Optional[Union[str, BasePromptTemplate]] = None,
        state_prompt: Optional[Union[str, BasePromptTemplate]] = None,
        timeout: Optional[float] = None,
        **workflow_kwargs: Any
    ):
        super().__init__(timeout=timeout, **workflow_kwargs)
        if not agent_configs:
            raise ValueError("At least one agent config must be provided")
        
        self.agent_configs = {cfg.name: cfg for cfg in agent_configs}
        only_one_root_agent = sum(cfg.is_root_agent for cfg in agent_configs) == 1
        if not only_one_root_agent:
            raise ValueError("Exactly one root agent must be provided")
        
        self.root_agent = next(cfg.name for cfg in agent_configs if cfg.is_root_agent)

        self.initial_state = initial_state or {}
        self.memory = memory or ChatMemoryBuffer.from_defaults(
            llm=Settings.llm or agent_configs[0].llm
        )
        self.handoff_prompt = handoff_prompt or DEFAULT_HANDOFF_PROMPT
        if isinstance(self.handoff_prompt, str):
            self.handoff_prompt = PromptTemplate(self.handoff_prompt)
        self.state_prompt = state_prompt
        if isinstance(self.state_prompt, str):
            self.state_prompt = PromptTemplate(self.state_prompt)

    def _ensure_tools_are_async(self, tools: List[BaseTool]) -> List[AsyncBaseTool]:
        """Ensure all tools are async."""
        return [adapt_to_async_tool(tool) for tool in tools]
    
    def _get_handoff_tool(self, current_agent_config: AgentConfig) -> AsyncBaseTool:
        """Creates a handoff tool for the given agent."""
        agent_info = {cfg.name: cfg.description for cfg in self.agent_configs.values()}

        # Filter out agents that the current agent cannot handoff to
        configs_to_remove = []
        for name in agent_info:
            if name == current_agent_config.name:
                configs_to_remove.append(name)
            elif current_agent_config.can_handoff_to is not None and name not in current_agent_config.can_handoff_to:
                configs_to_remove.append(name)

        for name in configs_to_remove:
            agent_info.pop(name)

        fn_tool_prompt = self.handoff_prompt.format(agent_info=str(agent_info))
        return FunctionTool.from_defaults(async_fn=handoff, description=fn_tool_prompt)

    async def _init_context(self, ctx: Context) -> None:
        """Initialize the context once, if needed."""
        if not await ctx.get("memory"):
            await ctx.set("memory", self.memory)
        if not await ctx.get("agent_configs"):
            await ctx.set("agent_configs", self.agent_configs)
        if not await ctx.get("current_state"):
            await ctx.set("current_state", self.initial_state)
        if not await ctx.get("current_agent"):
            await ctx.set("current_agent", self.root_agent)
            
    @step
    async def init_system(self, ctx: Context, ev: StartEvent) -> LLMInput:
        """Sets up the workflow and validates inputs."""
        await self._init_context(ctx)

        user_msg = ev.get("user_msg")
        chat_history = ev.get("chat_history")
        if user_msg and chat_history:
            raise ValueError("Cannot provide both user_msg and chat_history")
        
        if isinstance(user_msg, str):
            user_msg = ChatMessage(role="user", content=user_msg)

        if chat_history:
            chat_history = [user_msg]
        
        # Add messages to memory
        memory: BaseMemory = await ctx.get("memory")
        if user_msg: 
            input_messages = memory.get(input=user_msg.content) + [user_msg]
            memory.put(user_msg)
        else:
            memory.set(chat_history)
            input_messages = memory.get()
        
        # send to the current agent
        current_agent = await ctx.get("current_agent")
        return LLMInput(input=input_messages, current_agent=current_agent)
    
    def _call_function_calling_agent(self, llm: LLM, llm_input: List[ChatMessage], tools: List[AsyncBaseTool]) -> LLMOutput:
        """Call the LLM as a function calling agent."""
        pass

    def _call_react_agent(self, llm: LLM, llm_input: List[ChatMessage], tools: List[AsyncBaseTool]) -> LLMOutput:
        """Call the LLM as a react agent."""
        pass

    def _call_llm(self, llm: LLM, llm_input: List[ChatMessage], tools: List[AsyncBaseTool]) -> LLMOutput:
        """Call the LLM with the given input and tools."""
        if llm.metadata.is_function_calling_model:
            return self._call_function_calling_agent(llm, llm_input, tools)
        else:
            return self._call_react_agent(llm, llm_input, tools)
        
    @step
    async def setup_agent(
        self, ctx: Context, ev: LLMInput
    ) -> HandoffEvent | StopEvent:
        """Main agent handling logic."""
        agent_config: AgentConfig = (await ctx.get("agent_configs"))[ev.current_agent]
        current_state: dict = await ctx.get("current_state")
        llm_input = ev.input
        
        # Setup the tools
        tools = list(agent_config.tools or [])
        if agent_config.tool_retriever:
            retrieved_tools = await agent_config.tool_retriever.aretrieve(llm_input[-1].content or str(llm_input))
            tools.extend(retrieved_tools)
        

        handoff_tool = self._get_handoff_tool(agent_config)
        tools.append(handoff_tool)

        tools = self._ensure_tools_are_async(tools)

        # add the state to the llm input
        llm_input = [
            ChatMessage(
                role="system", 
                content=self.state_prompt.format(state=current_state) + "\n\n" + agent_config.system_prompt
            )
        ] + llm_input
        
        ctx.write_event_to_stream(LLMInput(input=llm_input, current_agent=ev.current_agent))

        return 
     