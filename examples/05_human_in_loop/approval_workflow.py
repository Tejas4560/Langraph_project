"""
Example 5: Human-in-the-Loop - Approval Workflow

This example demonstrates human-in-the-loop patterns in LangGraph:
- Using interrupts to pause execution
- Waiting for human approval
- State persistence with checkpoints
- Resuming from saved states
- Building approval workflows

Learning Focus: How to add human oversight and control to agent workflows

Note: This is a simplified example showing the concept. In production,
you would use LangGraph's built-in checkpointing with a database.
"""

import os
from typing import TypedDict, Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

# Load environment variables
load_dotenv()

# ============================================================================
# STEP 1: Define the State
# ============================================================================

class ContentState(TypedDict):
    """
    State for the content approval workflow.
    
    Fields:
        topic: The content topic
        draft: The drafted content
        feedback: Human feedback on the draft
        revision_count: Number of revisions made
        approved: Whether the content is approved
        final_content: The published content
    """
    topic: str
    draft: str
    feedback: str
    revision_count: int
    approved: bool
    final_content: str


# ============================================================================
# STEP 2: Initialize the LLM
# ============================================================================

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)


# ============================================================================
# STEP 3: Define Nodes
# ============================================================================

def draft_content(state: ContentState) -> ContentState:
    """
    Node 1: Draft initial content.
    
    This node creates the first draft of content based on the topic.
    """
    print("📍 Node: draft_content")
    print(f"   Topic: {state['topic']}")
    
    # Get current revision count
    revision_count = state.get("revision_count", 0)
    
    # Check if we have feedback (meaning this is a revision)
    has_feedback = bool(state.get("feedback"))
    
    if has_feedback:
        # This is a revision based on feedback
        system_msg = SystemMessage(content=f"""You are a content writer.
        Create a revised version of the content based on this feedback:
        {state['feedback']}
        
        Make sure to address all concerns raised and make it more engaging with specific examples.""")
        revision_count += 1  # Increment for this revision
        print(f"   ✓ Creating revision #{revision_count}")
    else:
        # This is the initial draft
        system_msg = SystemMessage(content="""You are a content writer.
        Create engaging, informative content on the given topic.
        Keep it concise but comprehensive (2-3 paragraphs).""")
        print(f"   ✓ Creating initial draft")
    
    user_msg = HumanMessage(content=f"Write content about: {state['topic']}")
    
    response = llm.invoke([system_msg, user_msg])
    draft = response.content
    
    return {
        "draft": draft,
        "revision_count": revision_count,
        "approved": False  # Reset approval status
    }


def request_approval(state: ContentState) -> ContentState:
    """
    Node 2: Request human approval.
    
    This node simulates requesting approval from a human.
    In a real application, this would:
    - Send the draft to a human reviewer
    - Wait for their response
    - Use LangGraph's interrupt() to pause execution
    
    For this example, we'll simulate the human decision.
    """
    print("📍 Node: request_approval")
    print("\n" + "=" * 70)
    print("📝 DRAFT CONTENT FOR APPROVAL:")
    print("=" * 70)
    print(state["draft"])
    print("=" * 70)
    
    # In a real application, you would use:
    # from langgraph.checkpoint import interrupt
    # human_response = interrupt("Please review and approve this content")
    
    # For this example, we'll simulate human approval
    # In practice, this would come from actual human input
    print("\n🤔 Simulating human review...")
    
    # Simulate: First draft gets rejected, first revision gets approved
    revision_count = state.get("revision_count", 0)
    if revision_count == 0:
        # First draft - reject it
        approved = False
        feedback = "Good start, but please make it more engaging and add specific examples."
        print("   ❌ Human Decision: REJECTED")
        print(f"   💬 Feedback: {feedback}")
    else:
        # Any revision - approve it
        approved = True
        feedback = "Looks great!"
        print("   ✅ Human Decision: APPROVED")
    
    return {
        "approved": approved,
        "feedback": feedback
    }


def publish_content(state: ContentState) -> ContentState:
    """
    Node 3: Publish the approved content.
    
    This node handles the final publication of approved content.
    """
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
    
    print("   ✓ Content published successfully!")
    
    return {
        "final_content": final_content
    }


# ============================================================================
# STEP 4: Define Routing Functions
# ============================================================================

def check_approval(state: ContentState) -> Literal["publish", "revise"]:
    """
    Routing function: Check if content was approved.
    
    Returns:
        "publish" if approved
        "revise" if rejected
    """
    if state.get("approved", False):
        print(f"\n🔀 Routing Decision: Content approved")
        print(f"   → Routing to: publish\n")
        return "publish"
    else:
        print(f"\n🔀 Routing Decision: Content needs revision")
        print(f"   → Routing to: revise\n")
        return "revise"


# ============================================================================
# STEP 5: Build the Graph
# ============================================================================

def create_approval_workflow():
    """
    Create and compile the approval workflow graph.
    
    Graph structure:
    
        START → draft_content → request_approval → [check_approval]
                     ↑                                    ↓
                     |                          ┌─────────┴─────────┐
                     |                          ↓                   ↓
                     └───────────────────── revise              publish
                                                                     ↓
                                                                    END
    
    The workflow loops until content is approved.
    """
    print("\n🔨 Building the approval workflow...")
    
    # Initialize the StateGraph
    graph = StateGraph(ContentState)
    
    # Add nodes
    graph.add_node("draft_content", draft_content)
    graph.add_node("request_approval", request_approval)
    graph.add_node("publish", publish_content)
    
    # Add edges
    graph.add_edge(START, "draft_content")
    graph.add_edge("draft_content", "request_approval")
    
    # Conditional edge based on approval
    graph.add_conditional_edges(
        "request_approval",
        check_approval,
        {
            "publish": "publish",
            "revise": "draft_content",  # Loop back to drafting
        }
    )
    
    graph.add_edge("publish", END)
    
    print("   ✓ Added 3 nodes: draft_content, request_approval, publish")
    print("   ✓ Added approval loop (revise → draft → approval)")
    print("   ✓ Human approval controls workflow progression")
    
    # Compile the graph
    # In production, you would add a checkpointer here:
    # from langgraph.checkpoint.memory import MemorySaver
    # app = graph.compile(checkpointer=MemorySaver())
    app = graph.compile()
    
    print("   ✓ Graph compiled successfully!\n")
    
    return app


# ============================================================================
# STEP 6: Run the Application
# ============================================================================

def run_approval_workflow(app, topic: str):
    """
    Run the approval workflow for a given topic.
    """
    print("=" * 70)
    print(f"📋 Content Topic: {topic}")
    print("=" * 70)
    
    # Create initial state
    initial_state = {
        "topic": topic,
        "draft": "",
        "feedback": "",
        "revision_count": 0,
        "approved": False,
        "final_content": ""
    }
    
    print("\n🔄 Starting approval workflow...\n")
    
    # Run the graph
    # The graph will loop until content is approved
    final_state = app.invoke(initial_state)
    
    print("\n" + "=" * 70)
    print("✅ Workflow Complete!")
    print("=" * 70)
    
    # Display the final published content
    print(final_state["final_content"])
    
    print(f"\n📊 Workflow Statistics:")
    print(f"   • Total revisions: {final_state['revision_count']}")
    print(f"   • Final status: {'Approved & Published' if final_state['approved'] else 'Pending'}")
    print("=" * 70 + "\n")


def main():
    """
    Main function to demonstrate the human-in-the-loop workflow.
    """
    print("=" * 70)
    print("🚀 Example 5: Human-in-the-Loop - Approval Workflow")
    print("=" * 70)
    
    # Create the approval workflow
    app = create_approval_workflow()
    
    # Test with a topic
    topic = "The Benefits of Learning LangGraph for AI Development"
    
    run_approval_workflow(app, topic)
    
    print("=" * 70)
    print("🎓 Key Learnings:")
    print("=" * 70)
    print("1. Human-in-the-loop adds oversight to agent workflows")
    print("2. Interrupts allow pausing execution for human input")
    print("3. Loops enable iterative refinement based on feedback")
    print("4. State persistence would allow resuming later (with checkpointer)")
    print("5. This pattern is essential for production AI applications")
    print("\n💡 Next Steps:")
    print("   • In production, use LangGraph's checkpointer for persistence")
    print("   • Implement actual interrupt() calls for real human input")
    print("   • Add timeout handling for approval requests")
    print("   • Build a web interface for human reviewers")
    print("=" * 70)


if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
    else:
        main()
