# Example 3: Tool-Calling Agent - Calculator Agent

## 🎯 Learning Objectives

In this example, you will learn:
- How to integrate **tools** with LangGraph agents
- The **ReAct pattern** (Reasoning + Acting)
- How agents decide when to use tools
- Building an agent reasoning loop
- Handling tool calls and responses

## 🧠 Concepts Covered

### 1. Tools
Tools are functions that agents can call to interact with the external world:
- Calculators
- Web search
- Database queries
- API calls
- File operations

### 2. ReAct Pattern
ReAct (Reasoning + Acting) is a pattern where the agent:
1. **Reasons** about what to do
2. **Acts** by calling a tool
3. **Observes** the result
4. **Repeats** until the task is complete

### 3. Agent Loop
The agent continuously decides:
- Should I call a tool?
- Which tool should I call?
- What arguments should I use?
- Is the task complete?

## 📝 The Code

The `calculator_agent.py` file implements an agent that:
1. Receives a math problem from the user
2. Decides if it needs to use the calculator tool
3. Calls the tool with appropriate arguments
4. Uses the result to formulate a final answer

The flow is cyclical:
```
START → agent_node → [should_continue?]
           ↑              ↓
           |         tool_node
           └──────────────┘
                ↓
               END
```

## 🚀 Running the Example

```bash
cd /home/lenovo/Langraph_Project
source venv/bin/activate
python examples/03_tool_calling_agent/calculator_agent.py
```

## 💡 What to Observe

When you run this example, notice:
1. How the agent decides to use tools
2. The reasoning process before calling tools
3. How tool results are incorporated
4. The loop continues until the task is complete

## 🔧 Experiment!

Try modifying the code:
- Add a new tool (e.g., string reverser, unit converter)
- Test with problems requiring multiple tool calls
- Change the agent's reasoning strategy
- Add error handling for invalid tool calls
- Create a tool that searches Wikipedia

## 📚 Key Takeaways

1. **Tools extend agent capabilities**: Agents can do more than just generate text
2. **ReAct is powerful**: Combining reasoning with actions creates capable agents
3. **Loops enable persistence**: Agents can work on complex multi-step tasks
4. **LangChain tools integrate seamlessly**: Rich ecosystem of pre-built tools

## ➡️ Next Steps

Once you understand tool-calling, move to Example 4 to learn about **multi-agent systems** and agent coordination!
