"""
LangGraph Learning Project - Web UI

A beautiful Streamlit interface to test all LangGraph examples interactively.
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="LangGraph Learning Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .example-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🚀 LangGraph Learning Hub</h1>', unsafe_allow_html=True)
st.markdown("### Interactive Web Interface for Testing LangGraph Examples")

# Check API key
if not os.getenv("GROQ_API_KEY"):
    st.error("⚠️ GROQ_API_KEY not found! Please add it to your .env file.")
    st.stop()

# Sidebar navigation
st.sidebar.title("📚 Navigation")
example_choice = st.sidebar.radio(
    "Choose an Example:",
    [
        "🏠 Home",
        "💬 Example 1: Basic Chatbot",
        "🎭 Example 2: Sentiment Router",
        "🔧 Example 3: Tool-Calling Agent",
        "👥 Example 4: Multi-Agent System",
        "✋ Example 5: Human-in-the-Loop",
        "🎯 Final Project: AI Research Assistant"
    ]
)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎓 About")
st.sidebar.info("""
This interactive UI lets you test all LangGraph examples without using the terminal.

**Powered by:**
- LangGraph
- Groq (Llama 3.3)
- Streamlit
""")

# Home page
if example_choice == "🏠 Home":
    st.markdown("## Welcome to the LangGraph Learning Hub! 👋")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 What You'll Learn
        
        This project teaches you LangGraph through 5 progressive examples:
        
        1. **Basic Chatbot** - Nodes, edges, state management
        2. **Sentiment Router** - Conditional routing
        3. **Tool-Calling Agent** - ReAct pattern with tools
        4. **Multi-Agent System** - Agent coordination
        5. **Human-in-the-Loop** - Approval workflows
        
        Plus a complete **AI Research Assistant** combining everything!
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Getting Started
        
        1. Select an example from the sidebar
        2. Enter your input or question
        3. Click "Run" to see LangGraph in action
        4. Observe the graph execution flow
        5. Learn from the results!
        
        **Status:** ✅ All systems ready!
        """)
    
    st.markdown("---")
    st.success("👈 Select an example from the sidebar to get started!")

# Example 1: Basic Chatbot
elif example_choice == "💬 Example 1: Basic Chatbot":
    st.markdown("## 💬 Example 1: Basic Chatbot")
    st.markdown("**Concepts:** Nodes, Edges, State Management")
    
    st.info("""
    This example demonstrates a simple linear graph with three nodes:
    1. **greet_user** - Initialize the conversation
    2. **process_message** - Call the LLM
    3. **format_response** - Format the output
    """)
    
    user_input = st.text_input(
        "Enter your message:",
        placeholder="Hello! Can you explain what LangGraph is?",
        key="example1_input"
    )
    
    if st.button("🚀 Run Example 1", key="example1_btn"):
        if user_input:
            with st.spinner("Processing through the graph..."):
                try:
                    # Import using importlib to handle numeric directory names
                    import importlib.util
                    import sys
                    
                    spec = importlib.util.spec_from_file_location(
                        "simple_chain",
                        "examples/01_basic_chatbot/simple_chain.py"
                    )
                    simple_chain = importlib.util.module_from_spec(spec)
                    sys.modules["simple_chain"] = simple_chain
                    spec.loader.exec_module(simple_chain)
                    
                    app = simple_chain.create_chatbot_graph()
                    
                    initial_state = {
                        "user_input": user_input,
                        "messages": [],
                        "response": "",
                        "metadata": {}
                    }
                    
                    final_state = app.invoke(initial_state)
                    
                    st.success("✅ Graph execution complete!")
                    
                    # Display results
                    st.markdown("### 🤖 Response:")
                    st.markdown(final_state["response"])
                    
                    # Display metadata
                    with st.expander("📊 View Execution Metadata"):
                        st.json(final_state["metadata"])
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please enter a message first!")

# Example 2: Sentiment Router
elif example_choice == "🎭 Example 2: Sentiment Router":
    st.markdown("## 🎭 Example 2: Sentiment Router")
    st.markdown("**Concepts:** Conditional Routing, Dynamic Flow")
    
    st.info("""
    This example routes your message to different response nodes based on sentiment:
    - 😊 **Positive** → Enthusiastic response
    - 💙 **Negative** → Empathetic response
    - 🤖 **Neutral** → Informative response
    """)
    
    user_input = st.text_area(
        "Enter your message:",
        placeholder="I'm so excited about learning LangGraph!",
        key="example2_input"
    )
    
    if st.button("🚀 Run Example 2", key="example2_btn"):
        if user_input:
            with st.spinner("Analyzing sentiment and routing..."):
                try:
                    import importlib.util
                    import sys
                    
                    spec = importlib.util.spec_from_file_location(
                        "sentiment_router",
                        "examples/02_conditional_routing/sentiment_router.py"
                    )
                    sentiment_router = importlib.util.module_from_spec(spec)
                    sys.modules["sentiment_router"] = sentiment_router
                    spec.loader.exec_module(sentiment_router)
                    
                    app = sentiment_router.create_sentiment_router()
                    
                    initial_state = {
                        "user_input": user_input,
                        "sentiment": "",
                        "response": "",
                        "confidence": 0.0
                    }
                    
                    final_state = app.invoke(initial_state)
                    
                    # Display sentiment
                    sentiment = final_state["sentiment"]
                    emoji = {"positive": "😊", "negative": "💙", "neutral": "🤖"}.get(sentiment, "🤖")
                    
                    st.success(f"✅ Detected Sentiment: {emoji} {sentiment.upper()}")
                    
                    # Display response
                    st.markdown("### Response:")
                    st.markdown(final_state["response"])
                    
                    # Display confidence
                    st.progress(final_state["confidence"])
                    st.caption(f"Confidence: {final_state['confidence']:.0%}")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please enter a message first!")

# Example 3: Tool-Calling Agent
elif example_choice == "🔧 Example 3: Tool-Calling Agent":
    st.markdown("## 🔧 Example 3: Tool-Calling Agent")
    st.markdown("**Concepts:** Tool Integration, ReAct Pattern")
    
    st.info("""
    This agent can use tools to solve problems:
    - 🧮 **Calculator** - Solve math problems
    - 📝 **Word Counter** - Count words in text
    """)
    
    user_input = st.text_input(
        "Ask the agent a question:",
        placeholder="What is 25 * 17 + 42?",
        key="example3_input"
    )
    
    if st.button("🚀 Run Example 3", key="example3_btn"):
        if user_input:
            with st.spinner("Agent is thinking and using tools..."):
                try:
                    import importlib.util
                    import sys
                    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
                    
                    spec = importlib.util.spec_from_file_location(
                        "calculator_agent",
                        "examples/03_tool_calling_agent/calculator_agent.py"
                    )
                    calculator_agent = importlib.util.module_from_spec(spec)
                    sys.modules["calculator_agent"] = calculator_agent
                    spec.loader.exec_module(calculator_agent)
                    
                    app = calculator_agent.create_agent_graph()
                    
                    initial_state = {
                        "messages": [
                            SystemMessage(content="You are a helpful assistant with access to tools."),
                            HumanMessage(content=user_input)
                        ]
                    }
                    
                    final_state = app.invoke(initial_state)
                    
                    st.success("✅ Agent completed the task!")
                    
                    # Get final response
                    final_response = None
                    tool_calls = 0
                    
                    for message in reversed(final_state["messages"]):
                        if isinstance(message, AIMessage):
                            if message.tool_calls:
                                tool_calls += 1
                            elif not final_response:
                                final_response = message.content
                    
                    st.markdown("### 🤖 Response:")
                    st.markdown(final_response)
                    
                    st.info(f"🔧 Tools used: {tool_calls} time(s)")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please enter a question first!")

# Example 4: Multi-Agent System
elif example_choice == "👥 Example 4: Multi-Agent System":
    st.markdown("## 👥 Example 4: Multi-Agent Research Team")
    st.markdown("**Concepts:** Multi-Agent Coordination, Specialized Roles")
    
    st.info("""
    A team of specialized agents collaborates on research:
    - 📋 **Supervisor** - Coordinates the team
    - 🔍 **Researcher** - Gathers information
    - 📊 **Analyst** - Analyzes findings
    - ✍️ **Writer** - Creates the report
    """)
    
    topic = st.text_input(
        "Enter a research topic:",
        placeholder="What is LangGraph and how does it work?",
        key="example4_input"
    )
    
    if st.button("🚀 Run Example 4", key="example4_btn"):
        if topic:
            with st.spinner("Research team is collaborating..."):
                try:
                    import importlib.util
                    import sys
                    
                    spec = importlib.util.spec_from_file_location(
                        "research_team",
                        "examples/04_multi_agent_system/research_team.py"
                    )
                    research_team = importlib.util.module_from_spec(spec)
                    sys.modules["research_team"] = research_team
                    spec.loader.exec_module(research_team)
                    
                    app = research_team.create_research_team()
                    
                    initial_state = {
                        "task": topic,
                        "messages": [],
                        "research_findings": "",
                        "analysis": "",
                        "final_report": "",
                        "next_agent": "supervisor",
                        "iteration": 0
                    }
                    
                    final_state = app.invoke(initial_state)
                    
                    st.success("✅ Research complete!")
                    
                    # Display report
                    st.markdown("### 📄 Final Report:")
                    st.markdown(final_state["final_report"])
                    
                    # Display stats
                    with st.expander("📊 Team Statistics"):
                        st.write(f"**Iterations:** {final_state['iteration']}")
                        st.write(f"**Research Length:** {len(final_state['research_findings'])} characters")
                        st.write(f"**Analysis Length:** {len(final_state['analysis'])} characters")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please enter a research topic first!")

# Example 5: Human-in-the-Loop
elif example_choice == "✋ Example 5: Human-in-the-Loop":
    st.markdown("## ✋ Example 5: Human-in-the-Loop Workflow")
    st.markdown("**Concepts:** Interrupts, Approval Workflows, Persistence")
    
    st.info("""
    This workflow demonstrates human oversight:
    1. Agent drafts content
    2. You review and approve/reject
    3. If rejected, agent revises based on feedback
    4. Loop continues until approved
    """)
    
    topic = st.text_input(
        "Enter a content topic:",
        placeholder="The Benefits of Learning LangGraph",
        key="example5_input"
    )
    
    if st.button("🚀 Start Workflow", key="example5_btn"):
        if topic:
            st.session_state.workflow_active = True
            st.session_state.topic = topic
            st.session_state.draft = None
            st.session_state.revision_count = 0
    
    if st.session_state.get("workflow_active"):
        with st.spinner("Generating draft..."):
            try:
                from langchain_groq import ChatGroq
                from langchain_core.messages import SystemMessage, HumanMessage
                
                llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
                
                if st.session_state.draft is None:
                    # Generate initial draft
                    system_msg = SystemMessage(content="You are a content writer. Create engaging, informative content on the given topic. Keep it concise but comprehensive (2-3 paragraphs).")
                    user_msg = HumanMessage(content=f"Write content about: {st.session_state.topic}")
                    response = llm.invoke([system_msg, user_msg])
                    st.session_state.draft = response.content
                
                st.markdown("### 📝 Draft Content:")
                st.markdown(st.session_state.draft)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Approve", key="approve_btn"):
                        st.success("🎉 Content approved and published!")
                        st.balloons()
                        st.session_state.workflow_active = False
                
                with col2:
                    if st.button("❌ Request Revision", key="reject_btn"):
                        feedback = st.text_area("Provide feedback for revision:", key="feedback_input")
                        if feedback:
                            # Generate revision
                            system_msg = SystemMessage(content=f"You are a content writer. Create a revised version based on this feedback: {feedback}")
                            user_msg = HumanMessage(content=f"Write content about: {st.session_state.topic}")
                            response = llm.invoke([system_msg, user_msg])
                            st.session_state.draft = response.content
                            st.session_state.revision_count += 1
                            st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Final Project
elif example_choice == "🎯 Final Project: AI Research Assistant":
    st.markdown("## 🎯 AI Research Assistant")
    st.markdown("**Combines All Concepts:** Complete Production-Ready Application")
    
    st.info("""
    This combines everything you've learned:
    - ✅ Task classification (simple vs complex)
    - ✅ Multi-agent collaboration
    - ✅ Tool integration
    - ✅ Conditional routing
    """)
    
    question = st.text_area(
        "Ask the research assistant:",
        placeholder="How can LangGraph be used to build production AI applications?",
        key="final_input"
    )
    
    if st.button("🚀 Run Research Assistant", key="final_btn"):
        if question:
            with st.spinner("Research assistant is working..."):
                try:
                    from final_project.ai_research_assistant import create_research_assistant
                    
                    app = create_research_assistant()
                    
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
                    
                    final_state = app.invoke(initial_state)
                    
                    st.success("✅ Research complete!")
                    
                    # Display report
                    st.markdown("### 📄 Research Report:")
                    st.markdown(final_state["final_report"])
                    
                    # Display classification
                    complexity_badge = "🔴 Complex" if final_state["complexity"] == "complex" else "🟢 Simple"
                    st.info(f"**Task Classification:** {complexity_badge}")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please enter a question first!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with ❤️ using LangGraph, Groq, and Streamlit</p>
    <p>🚀 Happy Learning!</p>
</div>
""", unsafe_allow_html=True)
