"""
Example 3: Tool-Calling Agent - Calculator Agent

This example demonstrates tool integration and the ReAct pattern in LangGraph:
- Integrating tools with agents
- The ReAct (Reasoning + Acting) pattern
- Agent reasoning loops
- Handling tool calls and responses
- Conditional routing based on agent decisions

Learning Focus: Building agents that can use external tools to solve problems
"""

import os
from typing import TypedDict, Annotated, Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# Load environment variables
load_dotenv()

# ============================================================================
# STEP 1: Define Tools
# ============================================================================
# Tools are functions that the agent can call to perform specific tasks.
# We use the @tool decorator to make them compatible with LangChain/LangGraph.

@tool
def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression and returns the result.
    
    Args:
        expression: A mathematical expression as a string (e.g., "25 * 17 + 42")
    
    Returns:
        The result of the calculation as a string
    
    Examples:
        calculator("2 + 2") -> "4"
        calculator("10 * 5 - 3") -> "47"
    """
    try:
        # Use eval for simple math (in production, use a safer alternative like ast.literal_eval)
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error calculating: {str(e)}"


@tool
def get_word_count(text: str) -> str:
    """
    Counts the number of words in a given text.
    
    Args:
        text: The text to count words in
    
    Returns:
        The number of words as a string
    """
    word_count = len(text.split())
    return str(word_count)


# List of all available tools
tools = [calculator, get_word_count]


# ============================================================================
# STEP 2: Define the State
# ============================================================================

class AgentState(TypedDict):
    """
    State for the tool-calling agent.
    
    Fields:
        messages: List of conversation messages (uses add_messages reducer)
                 The Annotated type with add_messages allows LangGraph to
                 automatically append new messages instead of replacing them
    """
    # The add_messages reducer automatically handles message list updates
    messages: Annotated[list, add_messages]


# ============================================================================
# STEP 3: Initialize the LLM with Tools
# ============================================================================

# Create the LLM and bind the tools to it
# This allows the LLM to know about and call these tools
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
llm_with_tools = llm.bind_tools(tools)


# ============================================================================
# STEP 4: Define Nodes
# ============================================================================

def agent_node(state: AgentState) -> AgentState:
    """
    The agent node: Decides what to do next.
    
    This node:
    1. Receives the current state (including conversation history)
    2. Calls the LLM to decide the next action
    3. The LLM can either:
       - Call a tool (returns a message with tool_calls)
       - Respond directly (returns a regular message)
    """
    print("📍 Node: agent_node")
    
    # The LLM will analyze the conversation and decide what to do
    response = llm_with_tools.invoke(state["messages"])
    
    # Check if the LLM wants to call a tool
    if response.tool_calls:
        print(f"   🔧 Agent decided to call tool: {response.tool_calls[0]['name']}")
        print(f"   📝 With arguments: {response.tool_calls[0]['args']}")
    else:
        print(f"   💬 Agent generated final response")
    
    # Return the updated state with the new message
    # The add_messages reducer will append this to the messages list
    return {"messages": [response]}


# We use LangGraph's prebuilt ToolNode for executing tools
# This node automatically handles tool calls from the agent
tool_node = ToolNode(tools)


# ============================================================================
# STEP 5: Define Routing Function
# ============================================================================

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """
    Routing function: Decides whether to continue to tools or end.
    
    This function checks the last message in the state:
    - If it contains tool_calls, route to the "tools" node
    - Otherwise, we're done, route to "end"
    
    Returns:
        "tools" if the agent wants to call a tool
        "end" if the agent is done
    """
    last_message = state["messages"][-1]
    
    # If the last message has tool calls, continue to tools
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        print(f"\n🔀 Routing Decision: Agent wants to use tools")
        print(f"   → Routing to: tools\n")
        return "tools"
    
    # Otherwise, we're done
    print(f"\n🔀 Routing Decision: Agent is finished")
    print(f"   → Routing to: end\n")
    return "end"


# ============================================================================
# STEP 6: Build the Graph
# ============================================================================

def create_agent_graph():
    """
    Create and compile the tool-calling agent graph.
    
    Graph structure (with loop):
    
        START → agent → [should_continue?]
                  ↑           ↓
                  |      ┌────┴────┐
                  |      ↓         ↓
                  └── tools       end → END
    
    The agent can call tools multiple times in a loop until it's satisfied.
    """
    print("\n🔨 Building the tool-calling agent graph...")
    
    # Initialize the StateGraph
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    
    # Add edges
    graph.add_edge(START, "agent")
    
    # Add conditional edge from agent
    # This is the key to the ReAct loop!
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",  # If agent wants to use tools, go to tools node
            "end": END,        # If agent is done, end the graph
        }
    )
    
    # After using tools, always go back to the agent
    # This creates the loop: agent → tools → agent → tools → ... → end
    graph.add_edge("tools", "agent")
    
    print("   ✓ Added 2 nodes: agent, tools")
    print("   ✓ Added conditional routing for ReAct loop")
    print("   ✓ Tools feed back to agent for iterative reasoning")
    
    # Compile the graph
    app = graph.compile()
    print("   ✓ Graph compiled successfully!\n")
    
    return app


# ============================================================================
# STEP 7: Run the Application
# ============================================================================

def test_agent(app, user_input: str):
    """
    Test the agent with a given input.
    """
    print("=" * 70)
    print(f"💬 User Input: {user_input}")
    print("─" * 70)
    
    # Create initial state with system message and user input
    initial_state = {
        "messages": [
            SystemMessage(content="""You are a helpful assistant with access to tools.
            When you need to perform calculations, use the calculator tool.
            When you need to count words, use the get_word_count tool.
            Always use tools when appropriate rather than trying to calculate in your head."""),
            HumanMessage(content=user_input)
        ]
    }
    
    print("🔄 Executing Agent Loop...\n")
    
    # Run the graph
    # The agent will loop until it's satisfied with the answer
    final_state = app.invoke(initial_state)
    
    print("─" * 70)
    print("✅ Agent Finished!")
    print("─" * 70)
    
    # Get the final response (last message that's not a tool message)
    final_response = None
    for message in reversed(final_state["messages"]):
        if isinstance(message, AIMessage) and not message.tool_calls:
            final_response = message.content
            break
    
    print(f"\n🤖 Final Response:\n{final_response}")
    print("\n" + "─" * 70)
    print(f"📊 Total messages in conversation: {len(final_state['messages'])}")
    
    # Count tool calls
    tool_calls = sum(1 for msg in final_state["messages"] if isinstance(msg, AIMessage) and msg.tool_calls)
    print(f"🔧 Tool calls made: {tool_calls}")
    print("=" * 70 + "\n")


def main():
    """
    Main function to demonstrate the tool-calling agent.
    """
    print("=" * 70)
    print("🚀 Example 3: Tool-Calling Agent - Calculator Agent")
    print("=" * 70)
    
    # Create the agent
    app = create_agent_graph()
    
    # Test cases
    test_cases = [
        "What is 25 multiplied by 17, plus 42?",
        "I need to know: (100 + 50) * 2 - 75",
        "How many words are in this sentence: 'LangGraph makes building agents easy and fun'?",
    ]
    
    print("🧪 Testing agent with different tasks...\n")
    
    for test_input in test_cases:
        test_agent(app, test_input)
    
    print("=" * 70)
    print("🎓 Key Learnings:")
    print("=" * 70)
    print("1. Tools extend what agents can do beyond text generation")
    print("2. The ReAct pattern (Reason → Act → Observe) is powerful")
    print("3. Conditional routing enables agent loops")
    print("4. Agents can use multiple tools to solve complex problems")
    print("5. The add_messages reducer simplifies state management")
    print("=" * 70)


if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
    else:
        main()
