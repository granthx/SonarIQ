from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Annotated
from graphs.workflow import build_graph

app = FastAPI()

# Allow the frontend (served from a different origin/port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Re-build graph with updated configuration and Strong/Cautious Go schemas
graph=build_graph()

# pydantic model for request body
class StartupIdea(BaseModel):
    startup_idea:Annotated[str,Field(...,description="Startup idea to validate")]

@app.get("/")
def read_root():
    return {"message": "Welcome to the SONARIQ API"}

@app.post("/validate")
async def research(idea:StartupIdea):
    try:
        result= await graph.ainvoke(
            {
                "startup_idea":idea.startup_idea,
                "market_analysis":None,
                "competition_analysis":None,
                "risk_assessment":None,
                "advisor_recommendations":None,
                "advice":None,
                "messages":[]
                })
        return JSONResponse(status_code=200, 
                            content={
                                "startup_idea": result["startup_idea"],
                                "market_analysis":result["market_analysis"],
                                "competition_analysis": result["competition_analysis"],
                                "risk_assessment": result["risk_assessment"],
                                "advisor_recommendations": result["advisor_recommendations"],
                                "advice": result["advice"]}
                            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))