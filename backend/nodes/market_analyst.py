from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Annotated,Literal
from langchain_core.messages import HumanMessage
from state.agent_state import AgentState
from models.chat_model import llm_with_tools,chat_model
from tools.web_search_tool import web_search
from config import MARKET_ANALYST_PROMPT_PATH

def analyze_market(preferred_mode:Literal["chat_model","tools"]="chat_model"):
    def market_analyzation(state:AgentState)->AgentState:
        """
        Creates a market analyst agent that can analyze market trends and provide insights.
        """
        try:
            template=open(MARKET_ANALYST_PROMPT_PATH).read()
        except FileNotFoundError:
            raise ValueError(f"Prompt file not found at {MARKET_ANALYST_PROMPT_PATH}. Please check the path and try again.")
        
        prompt_template = PromptTemplate(
            input_variables=["startup_idea"],
            template=template,
            )
        if preferred_mode == "chat_model":
            chain = prompt_template | chat_model
        else:
            chain = prompt_template | llm_with_tools
        response=chain.invoke({"startup_idea":state["startup_idea"]})
        if hasattr(response,"tool_calls") and response.tool_calls:
            return {"messages": [HumanMessage(state["startup_idea"]),response]}
        else:
            return {"market_analysis":response.content,"messages": [HumanMessage(state["startup_idea"]),response.content]}   
    return market_analyzation