# 🚀 LangGraph Hands-On Learning Project

Welcome! This project will teach you **LangGraph** through building 5 progressive examples and a complete AI Research Assistant.

## 📚 What is LangGraph?

LangGraph is a framework for building **stateful, multi-actor applications** with Large Language Models (LLMs). It extends LangChain by enabling you to create **cyclical graphs** where agents can:
- Maintain state across interactions
- Make dynamic decisions with conditional routing
- Use tools and external APIs
- Coordinate multiple specialized agents
- Include human-in-the-loop feedback

## 🎯 Learning Path

### Example 1: Basic Chatbot
**Concepts**: Nodes, Edges, State Management
- Build your first LangGraph application
- Understand the core building blocks
- Learn how state flows through the graph

### Example 2: Conditional Routing
**Concepts**: Conditional Edges, Dynamic Flow Control
- Implement sentiment analysis routing
- Learn how to make decisions in graphs
- Create branching workflows

### Example 3: Tool-Calling Agent
**Concepts**: Tool Integration, ReAct Pattern
- Build an agent that uses external tools
- Implement the reasoning-action loop
- Handle tool calls and responses

### Example 4: Multi-Agent System
**Concepts**: Agent Coordination, Specialized Roles
- Create a team of specialized agents
- Learn agent orchestration patterns
- Build supervisor-worker architectures

### Example 5: Human-in-the-Loop
**Concepts**: Interrupts, Persistence, Checkpoints
- Add human oversight to workflows
- Implement state persistence
- Resume from saved checkpoints

### Final Project: AI Research Assistant
**Combines All Concepts**
- Multi-agent research system
- Tool integration (web search, analysis)
- Human approval workflows
- Complete production-ready application

## 🛠️ Setup Instructions

### 1. Create Virtual Environment

```bash
cd /home/lenovo/Langraph_Project
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# You can get one at: https://platform.openai.com/api-keys
```

Your `.env` file should look like:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 4. Verify Installation

```bash
python -c "import langgraph; print('LangGraph version:', langgraph.__version__)"
```

## 🚦 Running the Examples

Each example is self-contained and can be run independently:

```bash
# Example 1: Basic Chatbot
python examples/01_basic_chatbot/simple_chain.py

# Example 2: Conditional Routing
python examples/02_conditional_routing/sentiment_router.py

# Example 3: Tool-Calling Agent
python examples/03_tool_calling_agent/calculator_agent.py

# Example 4: Multi-Agent System
python examples/04_multi_agent_system/research_team.py

# Example 5: Human-in-the-Loop
python examples/05_human_in_loop/approval_workflow.py

# Final Project: AI Research Assistant
python final_project/ai_research_assistant.py
```

## 📖 How to Learn

1. **Read the README** in each example folder first
2. **Run the example** to see it in action
3. **Read the code** with inline comments explaining each concept
4. **Modify the code** - experiment and break things!
5. **Complete the exercises** at the end of each example

## 🔑 Key LangGraph Concepts

### State
The shared data structure that flows through your graph. Each node can read and update the state.

```python
from typing import TypedDict

class GraphState(TypedDict):
    messages: list[str]
    user_input: str
```

### Nodes
Functions that process the state and return updates.

```python
def my_node(state: GraphState) -> GraphState:
    # Process state
    state["messages"].append("New message")
    return state
```

### Edges
Connections between nodes that define the flow.

```python
# Normal edge: always go from A to B
graph.add_edge("node_a", "node_b")

# Conditional edge: decide where to go based on state
graph.add_conditional_edges(
    "node_a",
    routing_function,  # Returns next node name
)
```

### Graph Compilation
Convert your graph definition into an executable application.

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(GraphState)
graph.add_node("my_node", my_node)
graph.add_edge(START, "my_node")
graph.add_edge("my_node", END)

app = graph.compile()
result = app.invoke({"user_input": "Hello"})
```

## 🎓 Best Practices

1. **Start Simple**: Begin with Example 1 and progress sequentially
2. **Understand State**: Always know what data is in your state
3. **Debug with Prints**: Add print statements to see state flow
4. **Visualize Graphs**: Use LangGraph's visualization tools
5. **Handle Errors**: Add try-except blocks in production code
6. **Test Incrementally**: Test each node individually first

## 🐛 Troubleshooting

### "Module not found" errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

### "API key not found" errors
```bash
# Check your .env file exists and has the correct key
cat .env
# Make sure you're loading it in your code:
from dotenv import load_dotenv
load_dotenv()
```

### Graph doesn't execute
- Check that all nodes are connected
- Verify START and END nodes are properly linked
- Ensure state type matches across all nodes

## 📚 Additional Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/tutorials/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## 🤝 Learning Tips

- **Take Notes**: Document what you learn in each example
- **Experiment**: Change parameters and see what happens
- **Build Your Own**: After completing examples, create your own agent
- **Ask Questions**: Understanding "why" is as important as "how"

## 📝 Project Structure

```
Langraph_Project/
├── README.md                    # This file
├── requirements.txt             # Dependencies
├── .env.example                 # Environment template
├── examples/                    # Learning examples
│   ├── 01_basic_chatbot/
│   ├── 02_conditional_routing/
│   ├── 03_tool_calling_agent/
│   ├── 04_multi_agent_system/
│   └── 05_human_in_loop/
└── final_project/               # Complete application
    └── ai_research_assistant.py
```

## 🎉 Ready to Start?

Begin with Example 1:
```bash
cd examples/01_basic_chatbot
cat README.md
python simple_chain.py
```

Happy learning! 🚀
