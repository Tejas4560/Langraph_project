"""
Example 4: Multi-Agent System - Research Team

This example demonstrates multi-agent coordination in LangGraph:
- Building specialized agents with different roles
- Supervisor-worker architecture
- Agent coordination and delegation
- State management across multiple agents
- Complex task decomposition

Learning Focus: How to build systems where multiple AI agents collaborate
"""

import os
from typing import TypedDict, Annotated, Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Load environment variables
load_dotenv()

# ============================================================================
# STEP 1: Define the State
# ============================================================================

class ResearchState(TypedDict):
    """
    State for the multi-agent research team.
    
    Fields:
        task: The research task/question
        messages: Conversation history
        research_findings: Information gathered by the researcher
        analysis: Insights from the analyst
        final_report: The completed report from the writer
        next_agent: Which agent should act next
        iteration: Current iteration count
    """
    task: str
    messages: Annotated[list, add_messages]
    research_findings: str
    analysis: str
    final_report: str
    next_agent: str
    iteration: int


# ============================================================================
# STEP 2: Initialize LLMs for Different Agents
# ============================================================================

# We can use different models or temperatures for different agents
supervisor_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
researcher_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
analyst_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5)
writer_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.6)


# ============================================================================
# STEP 3: Define Agent Nodes
# ============================================================================

def supervisor_node(state: ResearchState) -> ResearchState:
    """
    Supervisor Agent: Coordinates the team and decides next steps.
    
    The supervisor:
    - Reviews the current state
    - Decides which agent should act next
    - Determines if the task is complete
    """
    print("📍 Node: supervisor (Coordinator)")
    
    iteration = state.get("iteration", 0)
    
    # First iteration: start with researcher
    if iteration == 0:
        print("   🎯 Starting research process")
        print("   → Delegating to: researcher")
        return {
            "next_agent": "researcher",
            "iteration": iteration + 1
        }
    
    # Check what's been completed
    has_research = bool(state.get("research_findings"))
    has_analysis = bool(state.get("analysis"))
    has_report = bool(state.get("final_report"))
    
    print(f"   📊 Progress check:")
    print(f"      Research: {'✓' if has_research else '✗'}")
    print(f"      Analysis: {'✓' if has_analysis else '✗'}")
    print(f"      Report: {'✓' if has_report else '✗'}")
    
    # Decide next agent based on what's completed
    if not has_research:
        next_agent = "researcher"
    elif not has_analysis:
        next_agent = "analyst"
    elif not has_report:
        next_agent = "writer"
    else:
        next_agent = "FINISH"
    
    print(f"   → Delegating to: {next_agent}")
    
    return {
        "next_agent": next_agent,
        "iteration": iteration + 1
    }


def researcher_node(state: ResearchState) -> ResearchState:
    """
    Researcher Agent: Gathers information about the topic.
    
    In a real application, this agent would:
    - Search the web
    - Query databases
    - Read documents
    
    For this example, it uses the LLM's knowledge.
    """
    print("📍 Node: researcher (Information Gatherer)")
    
    system_msg = SystemMessage(content="""You are a research specialist.
    Your job is to gather comprehensive information about the given topic.
    Provide factual, detailed information that will be useful for analysis.
    Focus on key facts, statistics, and important context.""")
    
    user_msg = HumanMessage(content=f"Research this topic: {state['task']}")
    
    response = researcher_llm.invoke([system_msg, user_msg])
    
    findings = response.content
    print(f"   ✓ Gathered {len(findings)} characters of research")
    
    return {
        "research_findings": findings,
        "messages": [AIMessage(content=f"[Researcher] {findings[:100]}...")]
    }


def analyst_node(state: ResearchState) -> ResearchState:
    """
    Analyst Agent: Analyzes the research findings.
    
    This agent:
    - Reviews the research findings
    - Identifies patterns and insights
    - Draws conclusions
    """
    print("📍 Node: analyst (Data Analyzer)")
    
    system_msg = SystemMessage(content="""You are a data analyst and critical thinker.
    Your job is to analyze research findings and extract key insights.
    Look for patterns, implications, and important conclusions.
    Be analytical and objective.""")
    
    user_msg = HumanMessage(content=f"""Analyze these research findings about: {state['task']}
    
Research Findings:
{state['research_findings']}

Provide your analysis with key insights and conclusions.""")
    
    response = analyst_llm.invoke([system_msg, user_msg])
    
    analysis = response.content
    print(f"   ✓ Completed analysis ({len(analysis)} characters)")
    
    return {
        "analysis": analysis,
        "messages": [AIMessage(content=f"[Analyst] {analysis[:100]}...")]
    }


def writer_node(state: ResearchState) -> ResearchState:
    """
    Writer Agent: Creates the final polished report.
    
    This agent:
    - Reviews research and analysis
    - Creates a well-structured report
    - Ensures clarity and readability
    """
    print("📍 Node: writer (Report Creator)")
    
    system_msg = SystemMessage(content="""You are a professional writer and communicator.
    Your job is to create clear, well-structured reports.
    Synthesize the research and analysis into a coherent narrative.
    Make it engaging and easy to understand.""")
    
    user_msg = HumanMessage(content=f"""Create a comprehensive report about: {state['task']}

Research Findings:
{state['research_findings']}

Analysis:
{state['analysis']}

Write a clear, well-structured report that synthesizes this information.""")
    
    response = writer_llm.invoke([system_msg, user_msg])
    
    report = response.content
    print(f"   ✓ Report completed ({len(report)} characters)")
    
    return {
        "final_report": report,
        "messages": [AIMessage(content=f"[Writer] Report completed")]
    }


# ============================================================================
# STEP 4: Define Routing Function
# ============================================================================

def route_to_agent(state: ResearchState) -> Literal["supervisor", "researcher", "analyst", "writer", "end"]:
    """
    Routing function: Decides which agent should act next.
    
    The supervisor sets the "next_agent" field, and this function
    routes to that agent.
    """
    next_agent = state.get("next_agent", "supervisor")
    
    print(f"\n🔀 Routing Decision: next_agent='{next_agent}'")
    
    if next_agent == "FINISH":
        print(f"   → Routing to: end\n")
        return "end"
    elif next_agent in ["researcher", "analyst", "writer"]:
        print(f"   → Routing to: {next_agent}\n")
        return next_agent
    else:
        print(f"   → Routing to: supervisor\n")
        return "supervisor"


# ============================================================================
# STEP 5: Build the Graph
# ============================================================================

def create_research_team():
    """
    Create and compile the multi-agent research team graph.
    
    Graph structure:
    
        START → supervisor → [route_to_agent]
                   ↑              ↓
                   |      ┌───────┼───────┐
                   |      ↓       ↓       ↓
                   |  researcher analyst writer
                   |      └───────┼───────┘
                   └──────────────┘
                          ↓
                         end → END
    """
    print("\n🔨 Building the multi-agent research team...")
    
    # Initialize the StateGraph
    graph = StateGraph(ResearchState)
    
    # Add all agent nodes
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("writer", writer_node)
    
    # Start with the supervisor
    graph.add_edge(START, "supervisor")
    
    # Add conditional routing from supervisor
    graph.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "supervisor": "supervisor",
            "researcher": "researcher",
            "analyst": "analyst",
            "writer": "writer",
            "end": END,
        }
    )
    
    # All worker agents report back to supervisor
    graph.add_edge("researcher", "supervisor")
    graph.add_edge("analyst", "supervisor")
    graph.add_edge("writer", "supervisor")
    
    print("   ✓ Added 4 agent nodes: supervisor, researcher, analyst, writer")
    print("   ✓ Supervisor coordinates all agents")
    print("   ✓ Workers report back to supervisor after completing tasks")
    
    # Compile the graph
    app = graph.compile()
    print("   ✓ Graph compiled successfully!\n")
    
    return app


# ============================================================================
# STEP 6: Run the Application
# ============================================================================

def run_research_team(app, task: str):
    """
    Run the research team on a given task.
    """
    print("=" * 70)
    print(f"📋 Research Task: {task}")
    print("=" * 70)
    
    # Create initial state
    initial_state = {
        "task": task,
        "messages": [],
        "research_findings": "",
        "analysis": "",
        "final_report": "",
        "next_agent": "supervisor",
        "iteration": 0
    }
    
    print("\n🔄 Starting multi-agent collaboration...\n")
    
    # Run the graph
    final_state = app.invoke(initial_state)
    
    print("\n" + "=" * 70)
    print("✅ Research Complete!")
    print("=" * 70)
    
    # Display the final report
    print("\n📄 FINAL REPORT:")
    print("─" * 70)
    print(final_state["final_report"])
    print("─" * 70)
    
    print(f"\n📊 Team Statistics:")
    print(f"   • Total iterations: {final_state['iteration']}")
    print(f"   • Agents involved: Supervisor, Researcher, Analyst, Writer")
    print(f"   • Research length: {len(final_state['research_findings'])} characters")
    print(f"   • Analysis length: {len(final_state['analysis'])} characters")
    print(f"   • Report length: {len(final_state['final_report'])} characters")
    print("=" * 70 + "\n")


def main():
    """
    Main function to demonstrate the multi-agent research team.
    """
    print("=" * 70)
    print("🚀 Example 4: Multi-Agent System - Research Team")
    print("=" * 70)
    
    # Create the research team
    app = create_research_team()
    
    # Test with a research task
    task = "What is LangGraph and how does it differ from traditional LLM applications?"
    
    run_research_team(app, task)
    
    print("=" * 70)
    print("🎓 Key Learnings:")
    print("=" * 70)
    print("1. Multiple specialized agents can collaborate on complex tasks")
    print("2. A supervisor agent coordinates the workflow")
    print("3. Each agent has a specific role and expertise")
    print("4. State management allows agents to share information")
    print("5. This pattern scales well for complex applications")
    print("=" * 70)


if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
    else:
        main()
