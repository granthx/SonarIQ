from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode,tools_condition
import os
from langchain_core.messages import ToolMessage
from state.agent_state import AgentState
from nodes.market_analyst import analyze_market
from nodes.competitor_analysis import analyze_competition
from nodes.risk_assessor import assess_risk
from nodes.advisor import advisor
from tools.web_search_tool import web_search
from config import REPORTS_PATH,GRAPH_VISUALIZATION_PATH,ANALYSIS_LIST

def router(state:AgentState):       # Handles the routing logic after the tools node
    for analysis in ANALYSIS_LIST:
        if state[str(analysis)] is None:
            # if tool is failed
            if isinstance(state["messages"][-1],ToolMessage) and  state["messages"][-1].content=="tool_failed":
                if analysis == "market_analysis":
                    return_node="analyze_market_fallback"
                elif analysis == "competition_analysis":
                    return_node="analyze_competition_fallback"
                elif analysis == "risk_assessment":
                    return_node="assess_risk_fallback"
                break
                return f"{analysis}_fallback"
            else:
                if isinstance(state["messages"][-1],ToolMessage):
                    state[analysis]=state["messages"][-1].content
                
                if analysis == "market_analysis":
                    return_node="analyze_competition"
                elif analysis == "competition_analysis":
                    return_node="assess_risk"
                elif analysis == "risk_assessment":
                    return_node="advisor"
                break
    return return_node

def build_graph():
    try:
        graph_builder = StateGraph(AgentState)
        
        # define the nodes
        graph_builder.add_node("analyze_market",analyze_market(preferred_mode="tools"))
        graph_builder.add_node("analyze_competition",analyze_competition(preferred_mode="tools"))
        graph_builder.add_node("assess_risk",assess_risk(preferred_mode="tools"))

        # fallback nodes (chat_model only)
        graph_builder.add_node("analyze_market_fallback",analyze_market(preferred_mode="chat_model"))
        graph_builder.add_node("analyze_competition_fallback",analyze_competition(preferred_mode="chat_model"))
        graph_builder.add_node("assess_risk_fallback",assess_risk(preferred_mode="chat_model"))
        
        graph_builder.add_node("advisor", advisor)
        graph_builder.add_node("tools", ToolNode(tools=[web_search]))  # tools node for tool calls
        
        graph_builder.set_entry_point("analyze_market")     # entry point of the graph
        graph_builder.add_conditional_edges("analyze_market",tools_condition,{"tools": "tools","__end__":"analyze_competition"})  # condition to check if tools are needed
        graph_builder.add_conditional_edges("analyze_competition",tools_condition,{"tools": "tools","__end__":"assess_risk"})
        graph_builder.add_conditional_edges("assess_risk",tools_condition,{"tools": "tools","__end__":"advisor"})
        graph_builder.add_conditional_edges("tools",router)
        graph_builder.add_edge("analyze_market_fallback","analyze_competition")
        graph_builder.add_edge("analyze_competition_fallback","assess_risk")
        graph_builder.add_edge("assess_risk_fallback","advisor")

        graph_builder.add_edge("advisor", END)
        
        graph=graph_builder.compile()       # compile the graph
        
        return graph
    except Exception as e:
        print(f"Error in building graph: {e}")
        return None