"""
FastAPI Backend for LangGraph Learning Hub

Provides REST API endpoints for all LangGraph examples.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import sys
from dotenv import load_dotenv
import importlib.util

# Load environment variables
load_dotenv(dotenv_path="../../.env")

# Add parent directory to path to import examples
sys.path.append("../..")

app = FastAPI(
    title="LangGraph Learning Hub API",
    description="REST API for LangGraph examples",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class Example1Request(BaseModel):
    user_input: str

class Example2Request(BaseModel):
    user_input: str

class Example3Request(BaseModel):
    user_input: str

class Example4Request(BaseModel):
    topic: str

class Example5Request(BaseModel):
    topic: str
    feedback: Optional[str] = None

class FinalProjectRequest(BaseModel):
    question: str

class APIResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# Helper function to load modules dynamically
def load_module(module_name: str, file_path: str):
    """Dynamically load a Python module"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LangGraph Learning Hub API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    groq_key = os.getenv("GROQ_API_KEY")
    return {
        "status": "healthy",
        "groq_api_configured": bool(groq_key)
    }


@app.post("/api/example1", response_model=APIResponse)
async def example1(request: Example1Request):
    """
    Example 1: Basic Chatbot
    Linear graph with nodes, edges, and state management
    """
    try:
        # Load the module
        simple_chain = load_module(
            "simple_chain",
            "../../examples/01_basic_chatbot/simple_chain.py"
        )
        
        # Create and run the graph
        app_graph = simple_chain.create_chatbot_graph()
        
        initial_state = {
            "user_input": request.user_input,
            "messages": [],
            "response": "",
            "metadata": {}
        }
        
        final_state = app_graph.invoke(initial_state)
        
        return APIResponse(
            success=True,
            data={
                "response": final_state["response"],
                "metadata": final_state["metadata"]
            }
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=str(e)
        )


@app.post("/api/example2", response_model=APIResponse)
async def example2(request: Example2Request):
    """
    Example 2: Sentiment Router
    Conditional routing based on sentiment analysis
    """
    try:
        sentiment_router = load_module(
            "sentiment_router",
            "../../examples/02_conditional_routing/sentiment_router.py"
        )
        
        app_graph = sentiment_router.create_sentiment_router()
        
        initial_state = {
            "user_input": request.user_input,
            "sentiment": "",
            "response": "",
            "confidence": 0.0
        }
        
        final_state = app_graph.invoke(initial_state)
        
        return APIResponse(
            success=True,
            data={
                "sentiment": final_state["sentiment"],
                "response": final_state["response"],
                "confidence": final_state["confidence"]
            }
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=str(e)
        )


@app.post("/api/example3", response_model=APIResponse)
async def example3(request: Example3Request):
    """
    Example 3: Tool-Calling Agent
    Agent with tools using ReAct pattern
    """
    try:
        from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
        
        calculator_agent = load_module(
            "calculator_agent",
            "../../examples/03_tool_calling_agent/calculator_agent.py"
        )
        
        app_graph = calculator_agent.create_agent_graph()
        
        initial_state = {
            "messages": [
                SystemMessage(content="You are a helpful assistant with access to tools."),
                HumanMessage(content=request.user_input)
            ]
        }
        
        final_state = app_graph.invoke(initial_state)
        
        # Extract final response and tool usage
        final_response = None
        tool_calls = 0
        
        for message in reversed(final_state["messages"]):
            if isinstance(message, AIMessage):
                if message.tool_calls:
                    tool_calls += 1
                elif not final_response:
                    final_response = message.content
        
        return APIResponse(
            success=True,
            data={
                "response": final_response,
                "tool_calls": tool_calls
            }
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=str(e)
        )


@app.post("/api/example4", response_model=APIResponse)
async def example4(request: Example4Request):
    """
    Example 4: Multi-Agent System
    Research team with supervisor and specialized agents
    """
    try:
        research_team = load_module(
            "research_team",
            "../../examples/04_multi_agent_system/research_team.py"
        )
        
        app_graph = research_team.create_research_team()
        
        initial_state = {
            "task": request.topic,
            "messages": [],
            "research_findings": "",
            "analysis": "",
            "final_report": "",
            "next_agent": "supervisor",
            "iteration": 0
        }
        
        final_state = app_graph.invoke(initial_state)
        
        return APIResponse(
            success=True,
            data={
                "final_report": final_state["final_report"],
                "iterations": final_state["iteration"],
                "research_length": len(final_state["research_findings"]),
                "analysis_length": len(final_state["analysis"])
            }
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=str(e)
        )


@app.post("/api/example5", response_model=APIResponse)
async def example5(request: Example5Request):
    """
    Example 5: Human-in-the-Loop
    Content generation with approval workflow
    """
    try:
        from langchain_groq import ChatGroq
        from langchain_core.messages import SystemMessage, HumanMessage
        
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
        
        if request.feedback:
            # Generate revision based on feedback
            system_msg = SystemMessage(
                content=f"You are a content writer. Create a revised version based on this feedback: {request.feedback}"
            )
        else:
            # Generate initial draft
            system_msg = SystemMessage(
                content="You are a content writer. Create engaging, informative content on the given topic. Keep it concise but comprehensive (2-3 paragraphs)."
            )
        
        user_msg = HumanMessage(content=f"Write content about: {request.topic}")
        response = llm.invoke([system_msg, user_msg])
        
        return APIResponse(
            success=True,
            data={
                "draft": response.content,
                "is_revision": bool(request.feedback)
            }
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=str(e)
        )


@app.post("/api/final-project", response_model=APIResponse)
async def final_project(request: FinalProjectRequest):
    """
    Final Project: AI Research Assistant
    Complete application combining all concepts
    """
    try:
        ai_research = load_module(
            "ai_research_assistant",
            "../../final_project/ai_research_assistant.py"
        )
        
        app_graph = ai_research.create_research_assistant()
        
        initial_state = {
            "question": request.question,
            "complexity": "",
            "research_plan": "",
            "research_findings": "",
            "analysis": "",
            "final_report": "",
            "human_feedback": "",
            "approved": False,
            "messages": [],
            "iteration": 0
        }
        
        final_state = app_graph.invoke(initial_state)
        
        return APIResponse(
            success=True,
            data={
                "final_report": final_state["final_report"],
                "complexity": final_state["complexity"],
                "iterations": final_state["iteration"]
            }
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=str(e)
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
