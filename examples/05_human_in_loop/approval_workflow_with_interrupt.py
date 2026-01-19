"""
Example 5B: Human-in-the-Loop - WITH REAL INTERRUPTS

This demonstrates REAL interrupt() functionality in LangGraph.
Compare with approval_workflow.py to see the difference!

Key additions:
- interrupt() to pause execution
- MemorySaver checkpointer
- thread_id for tracking
- update_state() to resume
"""

import os
from typing import TypedDict, Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt

load_dotenv()

# State definition
class ContentState(TypedDict):
    topic: str
    draft: str
    feedback: str
    revision_count: int
    approved: bool
    final_content: str

# Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

# Nodes
def draft_content(state: ContentState) -> ContentState:
    """Create draft or revision"""
    print("📍 Node: draft_content")
    
    revision_count = state.get("revision_count", 0)
    has_feedback = bool(state.get("feedback"))
    
    if has_feedback:
        system_msg = SystemMessage(content=f"""You are a content writer.
        Revise based on this feedback: {state['feedback']}
        Address all concerns and add specific examples.""")
        revision_count += 1
        print(f"   ✓ Creating revision #{revision_count}")
    else:
        system_msg = SystemMessage(content="""You are a content writer.
        Create engaging, informative content (2-3 paragraphs).""")
        print(f"   ✓ Creating initial draft")
    
    user_msg = HumanMessage(content=f"Write about: {state['topic']}")
    draft = llm.invoke([system_msg, user_msg]).content
    
    return {"draft": draft, "revision_count": revision_count, "approved": False}

def request_approval(state: ContentState) -> ContentState:
    """⭐ THE KEY NODE - Uses interrupt() to PAUSE execution ⭐"""
    print("📍 Node: request_approval")
    print("\n" + "=" * 70)
    print("📝 DRAFT FOR APPROVAL:")
    print("=" * 70)
    print(state["draft"])
    print("=" * 70)
    
    # ⭐⭐⭐ INTERRUPT - EXECUTION PAUSES HERE ⭐⭐⭐
    print("\n⏸️  INTERRUPT: Pausing for human review...")
    print("   Graph execution STOPS here")
    print("   State saved to checkpointer")
    print("   Waiting for update_state() to resume\n")
    
    human_decision = interrupt(
        "Please review and provide:\n"
        "  - approved: True/False\n"
        "  - feedback: Your feedback"
    )
    
    # ⭐ EXECUTION RESUMES HERE ⭐
    print("\n▶️  RESUMED: Continuing with human decision...")
    
    if human_decision is None:
        return {"approved": False, "feedback": "No decision provided"}
    
    approved = human_decision.get("approved", False)
    feedback = human_decision.get("feedback", "")
    
    print(f"   {'✅ APPROVED' if approved else '❌ REJECTED'}")
    if not approved:
        print(f"   💬 Feedback: {feedback}")
    
    return {"approved": approved, "feedback": feedback}

def publish_content(state: ContentState) -> ContentState:
    """Publish approved content"""
    print("📍 Node: publish_content")
    
    final_content = f"""
╔══════════════════════════════════════════════════════════════════╗
║                     PUBLISHED CONTENT                            ║
╚══════════════════════════════════════════════════════════════════╝

Topic: {state['topic']}
Revisions: {state['revision_count']}

{state['draft']}

───────────────────────────────────────────────────────────────────
Status: ✅ Published
"""
    print("   ✓ Content published!")
    return {"final_content": final_content}

# Routing
def check_approval(state: ContentState) -> Literal["publish", "revise"]:
    """Route based on approval"""
    if state.get("approved", False):
        print("\n🔀 Routing: approved → publish\n")
        return "publish"
    else:
        print("\n🔀 Routing: rejected → revise\n")
        return "revise"

# Build graph
def create_approval_workflow():
    """Create graph WITH checkpointer (required for interrupts)"""
    print("\n🔨 Building workflow with INTERRUPTS enabled...")
    
    graph = StateGraph(ContentState)
    
    # Add nodes
    graph.add_node("draft_content", draft_content)
    graph.add_node("request_approval", request_approval)
    graph.add_node("publish", publish_content)
    
    # Add edges
    graph.add_edge(START, "draft_content")
    graph.add_edge("draft_content", "request_approval")
    graph.add_conditional_edges(
        "request_approval",
        check_approval,
        {"publish": "publish", "revise": "draft_content"}
    )
    graph.add_edge("publish", END)
    
    # ⭐ COMPILE WITH CHECKPOINTER - REQUIRED FOR INTERRUPTS ⭐
    checkpointer = MemorySaver()
    app = graph.compile(checkpointer=checkpointer)
    
    print("   ✓ Graph compiled with MemorySaver")
    print("   ✓ Interrupts enabled!\n")
    
    return app

# Run with interrupt handling
def run_with_interrupts(app, topic: str):
    """Run workflow with REAL interrupt handling"""
    print("=" * 70)
    print(f"📋 Topic: {topic}")
    print("=" * 70)
    
    # ⭐ thread_id tracks this conversation ⭐
    thread_id = "approval_001"
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "topic": topic,
        "draft": "",
        "feedback": "",
        "revision_count": 0,
        "approved": False,
        "final_content": ""
    }
    
    print("\n🔄 Starting workflow...\n")
    
    # Main loop - runs until completion
    while True:
        print("─" * 70)
        print("🚀 Invoking graph...")
        print("─" * 70 + "\n")
        
        # Run until interrupt or completion
        app.invoke(initial_state, config)
        
        # Check state
        state = app.get_state(config)
        
        # If no next nodes, we're done
        if not state.next:
            print("\n✅ Workflow completed!")
            break
        
        # We hit an interrupt
        print("\n" + "=" * 70)
        print("⏸️  PAUSED AT INTERRUPT")
        print("=" * 70)
        print(f"Waiting at: {state.next}")
        print("=" * 70)
        
        # Get human input
        print("\n👤 Your decision:")
        decision = input("Approve? (yes/no): ").strip().lower()
        
        if decision == "yes":
            human_decision = {"approved": True, "feedback": "Great!"}
            print("   ✅ Approved")
        else:
            feedback = input("Feedback: ").strip()
            human_decision = {"approved": False, "feedback": feedback}
            print(f"   ❌ Rejected: {feedback}")
        
        # ⭐ RESUME with update_state() ⭐
        print("\n▶️  Resuming...\n")
        app.update_state(config, human_decision, as_node="request_approval")
        
        # Continue from checkpoint
        initial_state = None
    
    # Show final result
    final_state = app.get_state(config)
    print("\n" + "=" * 70)
    print("✅ COMPLETE")
    print("=" * 70)
    print(final_state.values.get("final_content", ""))
    print(f"\n📊 Stats:")
    print(f"   • Revisions: {final_state.values.get('revision_count', 0)}")
    print("=" * 70 + "\n")

def main():
    print("=" * 70)
    print("🚀 Human-in-the-Loop WITH REAL INTERRUPTS")
    print("=" * 70)
    
    app = create_approval_workflow()
    topic = input("\nEnter topic: ")
    run_with_interrupts(app, topic)
    
    print("\n" + "=" * 70)
    print("🎓 Key Learnings:")
    print("=" * 70)
    print("1. interrupt() PAUSES execution")
    print("2. MemorySaver saves state")
    print("3. thread_id tracks conversation")
    print("4. update_state() resumes execution")
    print("5. Graph continues from exact pause point")
    print("=" * 70)

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found")
    else:
        main()
