# 🚀 Using Groq with LangGraph - Quick Guide

## ✅ Project Updated to Use Groq!

All examples now use **Groq** - a fast, efficient LLM provider with a generous free tier!

## 🔑 Setup Your API Key

### You Already Have a Groq API Key!

Since you mentioned you have a `GROQ_API_KEY` from a previous project, just add it to your `.env` file:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

**Replace `your_groq_api_key_here` with your actual Groq API key!**

## 🎯 Run Example 1

Once you've added your API key to the `.env` file:

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the first example
python examples/01_basic_chatbot/simple_chain.py
```

## 📊 What Changed?

| Component | Before (xAI) | Now (Groq) |
|-----------|--------------|------------|
| **Package** | `langchain-xai` | `langchain-groq` ✅ |
| **Class** | `ChatXAI` | `ChatGroq` ✅ |
| **Model** | `grok-beta` | `llama-3.3-70b-versatile` ✅ |
| **API Key** | `XAI_API_KEY` | `GROQ_API_KEY` ✅ |

## 🤖 Model Used

All examples now use **`llama-3.3-70b-versatile`**:
- Fast inference (Groq's specialty!)
- High quality responses
- Generous free tier
- Great for learning

## 💡 Why Groq?

- ✅ **Super Fast**: Groq's LPU technology makes inference incredibly fast
- ✅ **Free Tier**: Generous free usage limits
- ✅ **High Quality**: Uses Meta's Llama models
- ✅ **Easy to Use**: Simple API, works great with LangChain

## 📁 All Examples Updated

✅ Example 1: Basic Chatbot
✅ Example 2: Conditional Routing  
✅ Example 3: Tool-Calling Agent
✅ Example 4: Multi-Agent System
✅ Example 5: Human-in-the-Loop
✅ Final Project: AI Research Assistant

## 🔄 Your `.env` File Should Look Like:

```bash
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
```

**Note**: Groq API keys typically start with `gsk_`

## 🆘 Troubleshooting

**"GROQ_API_KEY not found"**
- Make sure `.env` file exists in `/home/lenovo/Langraph_Project/`
- Check that you added `GROQ_API_KEY=your-key` (no spaces around `=`)
- Verify virtual environment is activated

**"Authentication Error"**
- Verify your API key is correct
- Check it starts with `gsk_`
- Ensure you have credits on your Groq account

**Need a New API Key?**
- Go to: https://console.groq.com/
- Sign up or log in
- Create a new API key
- Copy and paste into `.env`

## 🎓 Ready to Learn!

Once your API key is in the `.env` file, you're ready to start learning LangGraph with Groq!

```bash
python examples/01_basic_chatbot/simple_chain.py
```

Happy learning! 🚀
