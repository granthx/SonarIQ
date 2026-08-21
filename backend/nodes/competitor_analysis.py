from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from typing import Literal
from state.agent_state import AgentState
from models.chat_model import llm_with_tools,chat_model
from config import COMPETITOR_ANALYSIS_PROMPT_PATH

def analyze_competition(preferred_mode: Literal["chat_model","tools"]="chat_model" ):
    def competition_analyzation(state: AgentState):
        """
        analyzes competition and provide insights.
        """
        try:
            template = open(COMPETITOR_ANALYSIS_PROMPT_PATH).read()
        except FileNotFoundError:
            raise ValueError(f"Prompt file not found at {COMPETITOR_ANALYSIS_PROMPT_PATH}. Please check the path and try again.")

        try:
            # Create a prompt template for the competitor analysis 
            prompt_template = PromptTemplate(
                input_variables=["startup_idea","market_analysis"],
                template=template,
            )
            if preferred_mode == "chat_model":
                chain = prompt_template | chat_model
            else:
                chain = prompt_template | llm_with_tools
            response=chain.invoke({"startup_idea":state["startup_idea"],"market_analysis":state["market_analysis"]})
            if hasattr(response,"tool_calls") and response.tool_calls:
                return {"messages": [response]}
            else:
                return {"competition_analysis":response.content,"messages": [response.content]}
        except Exception as e:
            raise ValueError(f"Error analyzing competition : {e}")
    return competition_analyzation