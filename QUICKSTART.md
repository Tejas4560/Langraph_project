# 🚀 LangGraph Quick Start Guide

## ⚡ Get Started in 3 Steps

### 1. Set Up Your API Key
```bash
cd /home/lenovo/Langraph_Project
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here
```

### 2. Activate Environment
```bash
source venv/bin/activate
```

### 3. Run Your First Example
```bash
python examples/01_basic_chatbot/simple_chain.py
```

## 📚 Learning Path

| Example | Concepts | File |
|---------|----------|------|
| **1. Basic Chatbot** | Nodes, Edges, State | `examples/01_basic_chatbot/simple_chain.py` |
| **2. Conditional Routing** | Dynamic routing, Branching | `examples/02_conditional_routing/sentiment_router.py` |
| **3. Tool-Calling Agent** | Tools, ReAct pattern | `examples/03_tool_calling_agent/calculator_agent.py` |
| **4. Multi-Agent System** | Agent coordination | `examples/04_multi_agent_system/research_team.py` |
| **5. Human-in-the-Loop** | Interrupts, Approval | `examples/05_human_in_loop/approval_workflow.py` |
| **Final Project** | All concepts combined | `final_project/ai_research_assistant.py` |

## 🎯 Core Patterns

### Basic Graph Structure
```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    message: str

def my_node(state: State) -> State:
    return {"message": "processed"}

graph = StateGraph(State)
graph.add_node("my_node", my_node)
graph.add_edge(START, "my_node")
graph.add_edge("my_node", END)
app = graph.compile()

result = app.invoke({"message": "hello"})
```

### Conditional Routing
```python
def route_function(state):
    if condition:
        return "node_a"
    else:
        return "node_b"

graph.add_conditional_edges(
    "source_node",
    route_function,
    {"node_a": "node_a", "node_b": "node_b"}
)
```

### Tool Integration
```python
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

@tool
def my_tool(input: str) -> str:
    """Tool description"""
    return f"Result: {input}"

llm_with_tools = llm.bind_tools([my_tool])
tool_node = ToolNode([my_tool])
```

## 💡 Tips

- **Read READMEs first**: Each example has detailed explanations
- **Check inline comments**: Code is heavily documented
- **Experiment**: Modify examples to learn
- **Progress sequentially**: Each example builds on previous ones

## 🆘 Troubleshooting

**"Module not found"**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**"API key not found"**
- Check `.env` file exists
- Verify `OPENAI_API_KEY` is set correctly

**Need help?**
- Check the main `README.md`
- Read example-specific READMEs
- Review the `walkthrough.md` in the artifacts folder

## 🎓 What You'll Learn

✅ State management in LangGraph
✅ Building multi-agent systems
✅ Tool integration and ReAct pattern
✅ Conditional routing and dynamic workflows
✅ Human-in-the-loop patterns
✅ Production-ready application design

## 🚀 Next Steps After Completion

1. Build your own LangGraph application
2. Explore [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
3. Join the LangChain community
4. Share your projects!

Happy learning! 🎉
