from langchain_community.tools import DuckDuckGoSearchRun,tool
import time
import random

@tool
def web_search(query: str) -> str:
    """
    Perform a web search using DuckDuckGo and return the results.
    
    Args:
        query (str): The search query.
        
    Returns:
        str: The search results.
    """
    try:
        search_tool = DuckDuckGoSearchRun()
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        result = search_tool.run(query)
        if not result or result.strip() == "":
            return "No search results found. Please try a different search query."
        return result
    except Exception as e:
        return "tool_failed"