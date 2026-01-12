"""
Example 2: Conditional Routing - Sentiment Router

This example demonstrates conditional edges and dynamic routing in LangGraph:
- Using conditional edges to make decisions
- Routing based on state content
- Creating branching workflows
- Multiple paths through a graph

Learning Focus: How to build graphs that adapt their behavior based on runtime data
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

class SentimentState(TypedDict):
    """
    State for the sentiment routing chatbot.
    
    Fields:
        user_input: The message from the user
        sentiment: Detected sentiment (positive, negative, neutral)
        response: The chatbot's response
        confidence: Confidence score for sentiment detection
    """
    user_input: str
    sentiment: str
    response: str
    confidence: float


# ============================================================================
# STEP 2: Initialize the LLM
# ============================================================================

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)


# ============================================================================
# STEP 3: Define Nodes
# ============================================================================

def analyze_sentiment(state: SentimentState) -> SentimentState:
    """
    Node 1: Analyze the sentiment of the user's input.
    
    This node uses the LLM to determine if the input is positive, negative, or neutral.
    The sentiment will be used by the routing function to decide the next node.
    """
    print("📍 Node: analyze_sentiment")
    print(f"   Input: {state['user_input']}")
    
    # Create a prompt for sentiment analysis
    system_msg = SystemMessage(content="""You are a sentiment analyzer. 
    Analyze the sentiment of the user's message and respond with ONLY one word:
    - 'positive' if the message is happy, excited, or optimistic
    - 'negative' if the message is sad, angry, or pessimistic  
    - 'neutral' if the message is neither positive nor negative
    
    Respond with only the single word, nothing else.""")
    
    user_msg = HumanMessage(content=state["user_input"])
    
    # Call the LLM for sentiment analysis
    response = llm.invoke([system_msg, user_msg])
    sentiment = response.content.strip().lower()
    
    # Validate the sentiment
    if sentiment not in ["positive", "negative", "neutral"]:
        sentiment = "neutral"  # Default to neutral if unclear
    
    state["sentiment"] = sentiment
    state["confidence"] = 0.85  # In a real app, you'd calculate this
    
    print(f"   ✓ Detected sentiment: {sentiment} (confidence: {state['confidence']:.2f})")
    return state


def positive_response(state: SentimentState) -> SentimentState:
    """
    Node 2a: Generate a positive, enthusiastic response.
    
    This node is called when the sentiment is positive.
    """
    print("📍 Node: positive_response")
    
    system_msg = SystemMessage(content="""You are an enthusiastic and upbeat AI assistant.
    The user is in a positive mood. Match their energy with an equally positive and 
    encouraging response. Be warm and supportive.""")
    
    user_msg = HumanMessage(content=state["user_input"])
    
    response = llm.invoke([system_msg, user_msg])
    state["response"] = f"😊 {response.content}"
    
    print(f"   ✓ Generated positive response")
    return state


def negative_response(state: SentimentState) -> SentimentState:
    """
    Node 2b: Generate an empathetic, supportive response.
    
    This node is called when the sentiment is negative.
    """
    print("📍 Node: negative_response")
    
    system_msg = SystemMessage(content="""You are an empathetic and supportive AI assistant.
    The user seems to be in a negative mood or facing challenges. Respond with empathy,
    understanding, and gentle encouragement. Offer support without being dismissive.""")
    
    user_msg = HumanMessage(content=state["user_input"])
    
    response = llm.invoke([system_msg, user_msg])
    state["response"] = f"💙 {response.content}"
    
    print(f"   ✓ Generated empathetic response")
    return state


def neutral_response(state: SentimentState) -> SentimentState:
    """
    Node 2c: Generate a balanced, informative response.
    
    This node is called when the sentiment is neutral.
    """
    print("📍 Node: neutral_response")
    
    system_msg = SystemMessage(content="""You are a helpful and professional AI assistant.
    The user's message is neutral or informational. Provide a clear, helpful, and 
    balanced response. Be friendly but professional.""")
    
    user_msg = HumanMessage(content=state["user_input"])
    
    response = llm.invoke([system_msg, user_msg])
    state["response"] = f"🤖 {response.content}"
    
    print(f"   ✓ Generated neutral response")
    return state


# ============================================================================
# STEP 4: Define Routing Function
# ============================================================================

def route_by_sentiment(state: SentimentState) -> Literal["positive_response", "negative_response", "neutral_response"]:
    """
    Routing function: Decides which response node to call based on sentiment.
    
    This function is called by the conditional edge to determine the next node.
    It examines the state and returns the name of the next node to execute.
    
    Returns:
        The name of the next node: "positive_response", "negative_response", or "neutral_response"
    """
    sentiment = state["sentiment"]
    
    print(f"\n🔀 Routing Decision: sentiment='{sentiment}'")
    
    # Map sentiment to the corresponding node
    if sentiment == "positive":
        print(f"   → Routing to: positive_response\n")
        return "positive_response"
    elif sentiment == "negative":
        print(f"   → Routing to: negative_response\n")
        return "negative_response"
    else:
        print(f"   → Routing to: neutral_response\n")
        return "neutral_response"


# ============================================================================
# STEP 5: Build the Graph
# ============================================================================

def create_sentiment_router():
    """
    Create and compile the sentiment routing graph.
    
    Graph structure:
                           START
                             ↓
                      analyze_sentiment
                             ↓
                    [conditional routing]
                             ↓
        ┌────────────────────┼────────────────────┐
        ↓                    ↓                    ↓
   positive_response   negative_response   neutral_response
        ↓                    ↓                    ↓
        └────────────────────┼────────────────────┘
                             ↓
                            END
    """
    print("\n🔨 Building the sentiment router graph...")
    
    # Initialize the StateGraph
    graph = StateGraph(SentimentState)
    
    # Add the sentiment analysis node
    graph.add_node("analyze_sentiment", analyze_sentiment)
    
    # Add the three response nodes
    graph.add_node("positive_response", positive_response)
    graph.add_node("negative_response", negative_response)
    graph.add_node("neutral_response", neutral_response)
    
    # Add normal edge from START to sentiment analysis
    graph.add_edge(START, "analyze_sentiment")
    
    # Add CONDITIONAL edge from sentiment analysis to response nodes
    # This is the key difference from Example 1!
    # The routing function decides which node to execute next
    graph.add_conditional_edges(
        "analyze_sentiment",  # Source node
        route_by_sentiment,   # Routing function that returns next node name
        {
            # Map the routing function's return values to actual nodes
            "positive_response": "positive_response",
            "negative_response": "negative_response",
            "neutral_response": "neutral_response",
        }
    )
    
    # All response nodes lead to END
    graph.add_edge("positive_response", END)
    graph.add_edge("negative_response", END)
    graph.add_edge("neutral_response", END)
    
    print("   ✓ Added 4 nodes: analyze_sentiment + 3 response nodes")
    print("   ✓ Added conditional routing based on sentiment")
    print("   ✓ All paths lead to END")
    
    # Compile the graph
    app = graph.compile()
    print("   ✓ Graph compiled successfully!\n")
    
    return app


# ============================================================================
# STEP 6: Run the Application
# ============================================================================

def test_sentiment_router(app, test_input: str):
    """
    Test the sentiment router with a given input.
    """
    print("=" * 70)
    print(f"💬 User Input: {test_input}")
    print("─" * 70)
    
    # Create initial state
    initial_state = {
        "user_input": test_input,
        "sentiment": "",
        "response": "",
        "confidence": 0.0
    }
    
    # Run the graph
    final_state = app.invoke(initial_state)
    
    print("─" * 70)
    print("✅ Response Generated!")
    print("─" * 70)
    print(final_state["response"])
    print("─" * 70)
    print(f"Sentiment: {final_state['sentiment']} (confidence: {final_state['confidence']:.2f})")
    print("=" * 70 + "\n")


def main():
    """
    Main function to demonstrate conditional routing.
    """
    print("=" * 70)
    print("🚀 Example 2: Conditional Routing - Sentiment Router")
    print("=" * 70)
    
    # Create the sentiment router
    app = create_sentiment_router()
    
    # Test with different sentiments
    test_cases = [
        "I just got promoted at work! I'm so excited and happy!",
        "I'm feeling really down today. Nothing seems to be going right.",
        "Can you explain how conditional routing works in LangGraph?",
    ]
    
    print("🧪 Testing with 3 different sentiments...\n")
    
    for test_input in test_cases:
        test_sentiment_router(app, test_input)
    
    print("=" * 70)
    print("🎓 Key Learnings:")
    print("=" * 70)
    print("1. Conditional edges enable dynamic routing based on state")
    print("2. Routing functions examine state and return the next node name")
    print("3. Different paths can be taken through the same graph")
    print("4. This pattern is powerful for building adaptive agents")
    print("=" * 70)


if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
    else:
        main()
