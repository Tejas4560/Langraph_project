# Example 2: Conditional Routing - Sentiment Router

## 🎯 Learning Objectives

In this example, you will learn:
- How to implement **conditional edges** for dynamic routing
- How to make decisions based on state
- How to create **branching workflows**
- How routing functions work in LangGraph

## 🧠 Concepts Covered

### 1. Conditional Edges
Unlike normal edges that always go from A to B, conditional edges decide where to go next based on the current state.

### 2. Routing Functions
Functions that examine the state and return the name of the next node to execute.

### 3. Branching Workflows
Graphs that can take different paths based on runtime conditions.

## 📝 The Code

The `sentiment_router.py` file implements a chatbot that:
1. **Analyzes** the sentiment of user input (positive, negative, neutral)
2. **Routes** to different response nodes based on sentiment
3. **Generates** appropriate responses for each sentiment type

The flow is dynamic:
```
START → analyze_sentiment → [routing decision]
                           ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
   positive_response  negative_response  neutral_response
        ↓                  ↓                  ↓
        └──────────────────┼──────────────────┘
                           ↓
                          END
```

## 🚀 Running the Example

```bash
cd /home/lenovo/Langraph_Project
source venv/bin/activate
python examples/02_conditional_routing/sentiment_router.py
```

## 💡 What to Observe

When you run this example, notice:
1. How the routing function examines the state
2. Different nodes execute based on sentiment
3. The graph can take multiple paths
4. Each path leads to the same end result

## 🔧 Experiment!

Try modifying the code:
- Add a new sentiment type (e.g., "excited", "confused")
- Create a corresponding response node
- Update the routing function to handle it
- Test with different user inputs
- Add more sophisticated sentiment analysis using the LLM

## 📚 Key Takeaways

1. **Conditional edges enable dynamic behavior**: Your graph can adapt based on runtime data
2. **Routing functions are powerful**: They give you full control over flow
3. **Multiple paths, same destination**: Different nodes can all lead to END
4. **State drives decisions**: The routing function uses state to decide the path

## ➡️ Next Steps

Once you understand conditional routing, move to Example 3 to learn about **tool-calling agents** and the ReAct pattern!
