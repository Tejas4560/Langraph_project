"""
Final Project: AI Research Assistant

This comprehensive application combines ALL concepts from Examples 1-5:
- State management and graph structure (Example 1)
- Conditional routing and dynamic decisions (Example 2)
- Tool integration and ReAct pattern (Example 3)
- Multi-agent coordination (Example 4)
- Human-in-the-loop workflows (Example 5)

This is a production-ready research assistant that can:
- Classify tasks by complexity
- Route simple questions to quick answers
- Coordinate multiple agents for complex research
- Use tools to gather information
- Incorporate human feedback and approval
"""

import os
from typing import TypedDict, Annotated, Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Load environment variables
load_dotenv()

# ============================================================================
# STEP 1: Define Tools
# ============================================================================

@tool
def web_search(query: str) -> str:
    """
    Simulates a web search for information.
    
    In a real application, this would use an actual search API like Tavily.
    
    Args:
        query: The search query
    
    Returns:
        Simulated search results
    """
    # This is a simulation. In production, use: from tavily import TavilyClient
    return f"""[Simulated Search Results for: {query}]
    
    1. LangGraph is a library for building stateful, multi-actor applications with LLMs
    2. It extends LangChain with the ability to create cyclical graphs
    3. Key features: state management, conditional routing, multi-agent systems
    4. Use cases: chatbots, autonomous agents, complex workflows
    5. Built by the LangChain team for production AI applications
    """


@tool
def analyze_document(text: str) -> str:
    """
    Analyzes a document and extracts key information.
    
    Args:
        text: The document text to analyze
    
    Returns:
        Analysis summary
    """
    word_count = len(text.split())
    char_count = len(text)
    
    return f"""Document Analysis:
    - Word count: {word_count}
    - Character count: {char_count}
    - Estimated reading time: {word_count // 200} minutes
    """


tools = [web_search, analyze_document]


# ============================================================================
# STEP 2: Define the State
# ============================================================================

class ResearchState(TypedDict):
    """
    Comprehensive state for the research assistant.
    """
    # User input
    question: str
    
    # Task classification
    complexity: str  # "simple" or "complex"
    
    # Research workflow
    research_plan: str
    research_findings: str
    analysis: str
    final_report: str
    
    # Human feedback
    human_feedback: str
    approved: bool
    
    # Metadata
    messages: Annotated[list, add_messages]
    iteration: int


# ============================================================================
# STEP 3: Initialize LLMs
# ============================================================================

# Different agents can have different configurations
classifier_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
planner_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5)
researcher_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
analyzer_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5)
writer_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.6)

# Bind tools to the researcher
researcher_llm_with_tools = researcher_llm.bind_tools(tools)


# ============================================================================
# STEP 4: Define Agent Nodes
# ============================================================================

def classify_task(state: ResearchState) -> ResearchState:
    """
    Classifier: Determines if the question is simple or complex.
    
    Simple questions get a quick answer.
    Complex questions go through the full research pipeline.
    """
    print("📍 Node: classify_task (Task Classifier)")
    
    system_msg = SystemMessage(content="""You are a task classifier.
    Determine if the user's question is SIMPLE or COMPLEX.
    
    SIMPLE: Can be answered directly with general knowledge (e.g., "What is LangGraph?")
    COMPLEX: Requires research, analysis, or multiple steps (e.g., "Compare LangGraph with other agent frameworks")
    
    Respond with only one word: SIMPLE or COMPLEX""")
    
    user_msg = HumanMessage(content=state["question"])
    
    response = classifier_llm.invoke([system_msg, user_msg])
    complexity = response.content.strip().upper()
    
    if complexity not in ["SIMPLE", "COMPLEX"]:
        complexity = "COMPLEX"  # Default to complex if unclear
    
    print(f"   ✓ Classified as: {complexity}")
    
    return {
        "complexity": complexity.lower(),
        "iteration": 0
    }


def quick_answer(state: ResearchState) -> ResearchState:
    """
    Quick Answer: Provides immediate response for simple questions.
    """
    print("📍 Node: quick_answer (Direct Response)")
    
    system_msg = SystemMessage(content="""You are a helpful AI assistant.
    Provide a clear, concise answer to the user's question.""")
    
    user_msg = HumanMessage(content=state["question"])
    
    response = researcher_llm.invoke([system_msg, user_msg])
    
    final_report = f"""
╔══════════════════════════════════════════════════════════════════╗
║                      QUICK ANSWER                                ║
╚══════════════════════════════════════════════════════════════════╝

Question: {state['question']}

{response.content}

───────────────────────────────────────────────────────────────────
Type: Simple Query | Status: ✅ Completed
"""
    
    print("   ✓ Generated quick answer")
    
    return {
        "final_report": final_report,
        "approved": True  # Auto-approve simple answers
    }


def planner_agent(state: ResearchState) -> ResearchState:
    """
    Planner: Creates a research plan for complex questions.
    """
    print("📍 Node: planner_agent (Research Planner)")
    
    system_msg = SystemMessage(content="""You are a research planner.
    Create a structured plan for researching the given question.
    Break it down into clear steps.""")
    
    user_msg = HumanMessage(content=f"Create a research plan for: {state['question']}")
    
    response = planner_llm.invoke([system_msg, user_msg])
    plan = response.content
    
    print(f"   ✓ Created research plan ({len(plan)} characters)")
    
    return {
        "research_plan": plan,
        "messages": [AIMessage(content=f"[Planner] {plan[:100]}...")]
    }


def researcher_agent(state: ResearchState) -> ResearchState:
    """
    Researcher: Gathers information using tools.
    """
    print("📍 Node: researcher_agent (Information Gatherer)")
    
    # Simulate using the web_search tool
    search_query = state["question"]
    search_results = web_search.invoke({"query": search_query})
    
    system_msg = SystemMessage(content=f"""You are a research specialist.
    Based on these search results, compile comprehensive research findings.
    
    Search Results:
    {search_results}
    
    Research Plan:
    {state.get('research_plan', 'No specific plan')}""")
    
    user_msg = HumanMessage(content=f"Research: {state['question']}")
    
    response = researcher_llm.invoke([system_msg, user_msg])
    findings = response.content
    
    print(f"   ✓ Gathered research findings ({len(findings)} characters)")
    
    return {
        "research_findings": findings,
        "messages": [AIMessage(content=f"[Researcher] Completed research")]
    }


def analyzer_agent(state: ResearchState) -> ResearchState:
    """
    Analyzer: Analyzes research findings and extracts insights.
    """
    print("📍 Node: analyzer_agent (Data Analyzer)")
    
    system_msg = SystemMessage(content="""You are a data analyst.
    Analyze the research findings and extract key insights, patterns, and conclusions.""")
    
    user_msg = HumanMessage(content=f"""Analyze these findings for: {state['question']}
    
    Research Findings:
    {state['research_findings']}""")
    
    response = analyzer_llm.invoke([system_msg, user_msg])
    analysis = response.content
    
    print(f"   ✓ Completed analysis ({len(analysis)} characters)")
    
    return {
        "analysis": analysis,
        "messages": [AIMessage(content=f"[Analyzer] Completed analysis")]
    }


def writer_agent(state: ResearchState) -> ResearchState:
    """
    Writer: Creates the final comprehensive report.
    """
    print("📍 Node: writer_agent (Report Writer)")
    
    system_msg = SystemMessage(content="""You are a professional report writer.
    Create a comprehensive, well-structured report synthesizing the research and analysis.""")
    
    user_msg = HumanMessage(content=f"""Create a report for: {state['question']}
    
    Research Findings:
    {state['research_findings']}
    
    Analysis:
    {state['analysis']}""")
    
    response = writer_llm.invoke([system_msg, user_msg])
    
    final_report = f"""
╔══════════════════════════════════════════════════════════════════╗
║                   RESEARCH REPORT                                ║
╚══════════════════════════════════════════════════════════════════╝

Question: {state['question']}

{response.content}

───────────────────────────────────────────────────────────────────
Research Team: Planner → Researcher → Analyzer → Writer
Status: ✅ Completed | Iterations: {state.get('iteration', 0)}
"""
    
    print(f"   ✓ Report completed ({len(final_report)} characters)")
    
    return {
        "final_report": final_report,
        "messages": [AIMessage(content=f"[Writer] Report completed")]
    }


def approval_node(state: ResearchState) -> ResearchState:
    """
    Approval: Simulates human approval of the final report.
    """
    print("📍 Node: approval_node (Human Review)")
    
    print("\n" + "=" * 70)
    print("📋 REPORT READY FOR APPROVAL")
    print("=" * 70)
    print(state["final_report"][:200] + "...")
    print("=" * 70)
    
    # In production, this would use interrupt() for real human input
    # For this demo, we auto-approve
    print("\n🤔 Simulating human review...")
    print("   ✅ Human Decision: APPROVED")
    
    return {
        "approved": True,
        "human_feedback": "Looks great!"
    }


# ============================================================================
# STEP 5: Define Routing Functions
# ============================================================================

def route_by_complexity(state: ResearchState) -> Literal["quick_answer", "planner"]:
    """
    Route based on task complexity.
    """
    complexity = state.get("complexity", "complex")
    
    print(f"\n🔀 Routing Decision: complexity='{complexity}'")
    
    if complexity == "simple":
        print(f"   → Routing to: quick_answer\n")
        return "quick_answer"
    else:
        print(f"   → Routing to: planner\n")
        return "planner"


# ============================================================================
# STEP 6: Build the Graph
# ============================================================================

def create_research_assistant():
    """
    Create the complete AI Research Assistant graph.
    
    This combines all concepts from Examples 1-5!
    """
    print("\n🔨 Building the AI Research Assistant...")
    
    graph = StateGraph(ResearchState)
    
    # Add all nodes
    graph.add_node("classify", classify_task)
    graph.add_node("quick_answer", quick_answer)
    graph.add_node("planner", planner_agent)
    graph.add_node("researcher", researcher_agent)
    graph.add_node("analyzer", analyzer_agent)
    graph.add_node("writer", writer_agent)
    graph.add_node("approval", approval_node)
    
    # Build the flow
    graph.add_edge(START, "classify")
    
    # Conditional routing based on complexity
    graph.add_conditional_edges(
        "classify",
        route_by_complexity,
        {
            "quick_answer": "quick_answer",
            "planner": "planner",
        }
    )
    
    # Simple path: quick_answer → END
    graph.add_edge("quick_answer", END)
    
    # Complex path: planner → researcher → analyzer → writer → approval → END
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "analyzer")
    graph.add_edge("analyzer", "writer")
    graph.add_edge("writer", "approval")
    graph.add_edge("approval", END)
    
    print("   ✓ Added 7 nodes with conditional routing")
    print("   ✓ Simple path: classify → quick_answer → END")
    print("   ✓ Complex path: classify → planner → researcher → analyzer → writer → approval → END")
    
    app = graph.compile()
    print("   ✓ Graph compiled successfully!\n")
    
    return app


# ============================================================================
# STEP 7: Run the Application
# ============================================================================

def research(app, question: str):
    """
    Run the research assistant on a question.
    """
    print("=" * 70)
    print(f"❓ Question: {question}")
    print("=" * 70)
    
    initial_state = {
        "question": question,
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
    
    print("\n🔄 Starting research assistant...\n")
    
    final_state = app.invoke(initial_state)
    
    print("\n" + "=" * 70)
    print("✅ Research Complete!")
    print("=" * 70)
    print(final_state["final_report"])
    print("=" * 70 + "\n")


def main():
    """
    Main function demonstrating the complete AI Research Assistant.
    """
    print("=" * 70)
    print("🚀 FINAL PROJECT: AI Research Assistant")
    print("=" * 70)
    print("\nThis project combines ALL concepts from Examples 1-5:")
    print("  ✅ State Management (Example 1)")
    print("  ✅ Conditional Routing (Example 2)")
    print("  ✅ Tool Integration (Example 3)")
    print("  ✅ Multi-Agent System (Example 4)")
    print("  ✅ Human-in-the-Loop (Example 5)")
    print("=" * 70)
    
    app = create_research_assistant()
    
    # Test with both simple and complex questions
    questions = [
        "What is LangGraph?",  # Simple
        "How can LangGraph be used to build production AI applications?",  # Complex
    ]
    
    for question in questions:
        research(app, question)
    
    print("=" * 70)
    print("🎓 Congratulations! You've completed the LangGraph learning project!")
    print("=" * 70)
    print("\nYou now know how to:")
    print("  • Build stateful AI applications")
    print("  • Create multi-agent systems")
    print("  • Integrate tools and APIs")
    print("  • Add human oversight")
    print("  • Build production-ready LangGraph apps")
    print("\n🚀 Next: Build your own LangGraph application!")
    print("=" * 70)


if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found")
        print("Please create a .env file with your OpenAI API key")
    else:
        main()
