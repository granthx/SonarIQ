from langchain_groq import ChatGroq
from tools.web_search_tool import web_search
import os
from dotenv import load_dotenv
from config import REPO_ID, TEMPERATURE, MAX_NEW_TOKENS
load_dotenv()

tools_list=[web_search]
api_key=os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

chat_model=ChatGroq(
    model=REPO_ID,
    max_tokens=MAX_NEW_TOKENS,
    temperature=TEMPERATURE,
    api_key=api_key
)
llm_with_tools=chat_model.bind_tools(tools_list)