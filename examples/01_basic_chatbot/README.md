# Example 1: Basic Chatbot - Linear Graph

## 🎯 Learning Objectives

In this example, you will learn:
- How to define a **StateGraph** with typed state
- How to create **nodes** (functions that process state)
- How to add **edges** to connect nodes
- How to **compile** and **run** a graph
- Understanding the flow of data through a LangGraph application

## 🧠 Concepts Covered

### 1. State Management
State is the central data structure that flows through your graph. It's like a shared memory that all nodes can read and update.

### 2. Nodes
Nodes are functions that:
- Take the current state as input
- Perform some operation (call an LLM, process data, etc.)
- Return updated state

### 3. Edges
Edges define the flow between nodes:
- **Normal edges**: Direct connections (A → B)
- **START**: Entry point of the graph
- **END**: Exit point of the graph

## 📝 The Code

The `simple_chain.py` file implements a basic chatbot with three nodes:
1. **greet_user**: Welcomes the user
2. **process_message**: Calls the LLM to generate a response
3. **format_response**: Formats the final output

The flow is linear: START → greet_user → process_message → format_response → END

## 🚀 Running the Example

```bash
# Make sure you're in the project root and virtual environment is activated
cd /home/lenovo/Langraph_Project
source venv/bin/activate

# Run the example
python examples/01_basic_chatbot/simple_chain.py
```

## 💡 What to Observe

When you run this example, notice:
1. How state is passed between nodes
2. Each node adds information to the state
3. The final state contains all accumulated data
4. The linear flow from start to end

## 🔧 Experiment!

Try modifying the code:
- Add a new node that counts words in the response
- Change the system prompt to make the chatbot more formal/casual
- Add more fields to the state (e.g., timestamp, user_name)
- Print the state after each node to see how it evolves

## 📚 Key Takeaways

1. **State is central**: Everything flows through the state object
2. **Nodes are pure functions**: They take state and return updated state
3. **Graphs are declarative**: You define the structure, LangGraph handles execution
4. **Type safety**: Using TypedDict helps catch errors early

## ➡️ Next Steps

Once you understand this example, move to Example 2 to learn about **conditional routing** and dynamic decision-making!
