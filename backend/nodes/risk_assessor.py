from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from typing import Literal
from state.agent_state import AgentState
from models.chat_model import llm_with_tools,chat_model
import os
from tools.web_search_tool import web_search
from config import RISK_ASSESSOR_PROMPT_PATH

def assess_risk(preferred_mode: Literal["chat_model","tools"]="chat_model"):
    def assessment_risk(state: AgentState) -> AgentState:
        """
        Analyzes risk factors and provide trends and insights.
        """
        if not os.path.exists(RISK_ASSESSOR_PROMPT_PATH):
            raise FileNotFoundError(f"Prompt file not found at {RISK_ASSESSOR_PROMPT_PATH}. Please check the path and try again.")
        try:
            template = open(RISK_ASSESSOR_PROMPT_PATH).read()
        except FileNotFoundError:
            raise ValueError(f"Prompt file not found at {RISK_ASSESSOR_PROMPT_PATH}. Please check the path and try again.")
        
        # Create a prompt template for the risk assessment
        prompt_template = PromptTemplate(
            input_variables=["startup_idea", "market_analysis", "competition_analysis"],
            template=template,
            )
        if preferred_mode == "chat_model":
            chain = prompt_template | chat_model
        else:
            chain = prompt_template | llm_with_tools
        response = chain.invoke({
            "startup_idea": state["startup_idea"],
            "market_analysis": state["market_analysis"],
            "competition_analysis": state["competition_analysis"]
            })
        if hasattr(response,"tool_calls") and response.tool_calls:
            return {"messages": [response]}
        else:
            return {"risk_assessment":response.content,"messages": [response.content]} 
    return assessment_risk