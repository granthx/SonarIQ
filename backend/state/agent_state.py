from typing import TypedDict, List, Optional
from pydantic import Field
from langchain_core.messages import BaseMessage

#State model for the agent
class AgentState(TypedDict):
    startup_idea: str
    market_analysis: Optional[str]
    competition_analysis: Optional[str]
    risk_assessment: Optional[str]
    advisor_recommendations: Optional[str]
    advice: Optional[str]
    messages: List[BaseMessage]