from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel,Field
from typing import Literal,Annotated
from state.agent_state import AgentState
from models.chat_model import chat_model
from config import ADVISOR_PROMPT_PATH
import os

class AdvisorSchema(BaseModel):
    """
    Schema for the advisor response.
    """
    advisor_recommendations: Annotated[Literal["Strong Go","No-Go","Cautious Go"], Field(description="The decision made by the advisor based on the analysis. whether to proceed with the startup idea or not.")]
    advice: Annotated[str,Field(description="Advice or suggestions or reasons provided by the advisor based on the analysis. This should include why the decision is 'Strong Go' or 'Cautious Go', or reasons for 'No-Go'.")]
    
def advisor(state:AgentState)-> AgentState:
    """
    Analyzes market,competition ,risk and provides the advice.
    """
    if not os.path.exists(ADVISOR_PROMPT_PATH):
        raise ValueError(f"Prompt file not found at {ADVISOR_PROMPT_PATH}. Please check the path and try again.")
    
    try: 
        template=open(ADVISOR_PROMPT_PATH).read()
        prompt_text = template.format(
            startup_idea=state["startup_idea"],
            market_analysis=state["market_analysis"],
            competition_analysis=state["competition_analysis"],
            risk_assessment=state["risk_assessment"],
            format_instructions=""
        )
        structured_llm = chat_model.with_structured_output(AdvisorSchema)
        response = structured_llm.invoke(prompt_text)
        return {"advisor_recommendations": response.advisor_recommendations, "advice": response.advice}
        
    except Exception as e:
        raise ValueError(f"Error advising : {e}")