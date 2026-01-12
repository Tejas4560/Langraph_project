"""
Example 1: Basic Chatbot - Linear Graph

This example demonstrates the fundamental building blocks of LangGraph:
- Defining state with TypedDict
- Creating nodes (functions that process state)
- Adding edges to connect nodes
- Compiling and running the graph

Learning Focus: Understanding how data flows through a LangGraph application
"""

import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

# Load environment variables (API keys)
load_dotenv()

# ============================================================================
# STEP 1: Define the State
# ============================================================================
# State is the shared data structure that flows through the graph.
# Each node can read from and write to the state.

class ChatbotState(TypedDict):
    """
    The state of our chatbot application.
    
    Fields:
        user_input: The message from the user
        messages: List of conversation messages
        response: The final chatbot response
        metadata: Additional information about the conversation
    """
    user_input: str
    messages: list
    response: str
    metadata: dict


# ============================================================================
# STEP 2: Initialize the LLM
# ============================================================================
# We'll use xAI's Grok model for generating responses

llm = ChatGroq(
    model="llama-3.3-70b-versatile",     # Using Grok's beta model
    temperature=0.7,       # Controls randomness (0=deterministic, 1=creative)
)


# ============================================================================
# STEP 3: Define Nodes (Functions that process state)
# ============================================================================

def greet_user(state: ChatbotState) -> ChatbotState:
    """
    Node 1: Greet the user and initialize the conversation.
    
    This node:
    - Adds a system message to set the chatbot's behavior
    - Initializes metadata
    - Returns the updated state
    """
    print("📍 Node: greet_user")
    
    # Add a system message to define the chatbot's personality
    system_msg = SystemMessage(content="You are a helpful and friendly AI assistant.")
    
    # Update the state
    state["messages"] = [system_msg]
    state["metadata"] = {
        "conversation_started": True,
        "node_count": 1
    }
    
    print(f"   ✓ Initialized conversation with system message")
    return state


def process_message(state: ChatbotState) -> ChatbotState:
    """
    Node 2: Process the user's message and generate a response.
    
    This node:
    - Adds the user's message to the conversation
    - Calls the LLM to generate a response
    - Updates the state with the response
    """
    print("📍 Node: process_message")
    
    # Add the user's message to the conversation
    user_msg = HumanMessage(content=state["user_input"])
    state["messages"].append(user_msg)
    
    print(f"   ✓ User input: {state['user_input']}")
    
    # Call the LLM with the conversation history
    response = llm.invoke(state["messages"])
    
    # Store the response
    state["response"] = response.content
    state["messages"].append(response)
    
    # Update metadata
    state["metadata"]["node_count"] = 2
    state["metadata"]["response_length"] = len(response.content)
    
    print(f"   ✓ Generated response ({len(response.content)} characters)")
    return state


def format_response(state: ChatbotState) -> ChatbotState:
    """
    Node 3: Format the final response.
    
    This node:
    - Adds formatting to the response
    - Updates final metadata
    - Returns the completed state
    """
    print("📍 Node: format_response")
    
    # Add some formatting to the response
    formatted = f"🤖 Assistant: {state['response']}"
    state["response"] = formatted
    
    # Update metadata
    state["metadata"]["node_count"] = 3
    state["metadata"]["conversation_completed"] = True
    
    print(f"   ✓ Response formatted and ready")
    return state


# ============================================================================
# STEP 4: Build the Graph
# ============================================================================

def create_chatbot_graph():
    """
    Create and compile the chatbot graph.
    
    Graph structure:
    START → greet_user → process_message → format_response → END
    
    This is a linear graph where each node processes the state in sequence.
    """
    print("\n🔨 Building the graph...")
    
    # Initialize the StateGraph with our state type
    graph = StateGraph(ChatbotState)
    
    # Add nodes to the graph
    # Each node is a function that takes state and returns updated state
    graph.add_node("greet_user", greet_user)
    graph.add_node("process_message", process_message)
    graph.add_node("format_response", format_response)
    
    # Add edges to define the flow
    # START is a special marker for the entry point
    graph.add_edge(START, "greet_user")
    graph.add_edge("greet_user", "process_message")
    graph.add_edge("process_message", "format_response")
    # END is a special marker for the exit point
    graph.add_edge("format_response", END)
    
    print("   ✓ Added 3 nodes: greet_user, process_message, format_response")
    print("   ✓ Added 4 edges to create linear flow")
    
    # Compile the graph into an executable application
    app = graph.compile()
    print("   ✓ Graph compiled successfully!\n")
    
    return app


# ============================================================================
# STEP 5: Run the Application
# ============================================================================

def main():
    """
    Main function to run the chatbot example.
    """
    print("=" * 70)
    print("🚀 Example 1: Basic Chatbot - Linear Graph")
    print("=" * 70)
    
    # Create the chatbot application
    app = create_chatbot_graph()
    
    # Define initial state
    initial_state = {
        "user_input": "Hello! Can you explain what LangGraph is in simple terms?",
        "messages": [],
        "response": "",
        "metadata": {}
    }
    
    print("💬 User Input:", initial_state["user_input"])
    print("\n" + "─" * 70)
    print("🔄 Executing Graph...")
    print("─" * 70 + "\n")
    
    # Invoke the graph with the initial state
    # The graph will execute all nodes in sequence
    final_state = app.invoke(initial_state)
    
    print("\n" + "─" * 70)
    print("✅ Graph Execution Complete!")
    print("─" * 70 + "\n")
    
    # Display the results
    print("📊 RESULTS:")
    print("─" * 70)
    print(final_state["response"])
    print("─" * 70)
    print(f"\n📈 Metadata:")
    print(f"   • Nodes executed: {final_state['metadata']['node_count']}")
    print(f"   • Response length: {final_state['metadata']['response_length']} characters")
    print(f"   • Conversation completed: {final_state['metadata']['conversation_completed']}")
    print(f"   • Total messages: {len(final_state['messages'])}")
    
    print("\n" + "=" * 70)
    print("🎓 Key Learnings:")
    print("=" * 70)
    print("1. State flows through each node sequentially")
    print("2. Each node can read and update the state")
    print("3. The graph structure is defined declaratively")
    print("4. LangGraph handles the execution flow automatically")
    print("=" * 70)


if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in environment variables")
        print("Please create a .env file with your Groq API key")
        print("Get your API key at: https://console.groq.com/")
    else:
        main()

