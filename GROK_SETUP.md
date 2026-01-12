# 🤖 Using Grok (xAI) with LangGraph

## ✅ Project Updated!

All examples in this project have been updated to use **xAI's Grok** instead of OpenAI!

## 🔑 Getting Your Grok API Key

1. **Visit**: https://console.x.ai/
2. **Sign up** or log in to your xAI account
3. **Create an API key** in the console
4. **Copy** your API key (starts with `xai-`)

## 📝 Setup Instructions

### 1. Add Your API Key to `.env`

Edit your `.env` file and add:
```bash
XAI_API_KEY=xai-your-actual-api-key-here
```

### 2. Run the Examples

```bash
# Activate virtual environment
source venv/bin/activate

# Run Example 1
python examples/01_basic_chatbot/simple_chain.py
```

## 🆚 Grok vs OpenAI

### Why Grok?
- ✅ Competitive pricing
- ✅ Strong performance
- ✅ Access to real-time information
- ✅ Built by xAI (Elon Musk's AI company)

### Model Used
All examples use **`grok-beta`** - Grok's latest model with strong capabilities.

## 📦 What Was Changed?

1. **Dependencies**: 
   - Removed: `langchain-openai`
   - Added: `langchain-xai`

2. **Code Updates**:
   - Changed: `from langchain_openai import ChatOpenAI`
   - To: `from langchain_xai import ChatXAI`
   
3. **Model Configuration**:
   - Changed: `model="gpt-4o-mini"`
   - To: `model="grok-beta"`

4. **Environment Variable**:
   - Changed: `OPENAI_API_KEY`
   - To: `XAI_API_KEY`

## 🔄 Switching Back to OpenAI (Optional)

If you want to switch back to OpenAI later:

```bash
# Install OpenAI package
pip install langchain-openai

# Update code manually or use find-replace:
# ChatXAI → ChatOpenAI
# grok-beta → gpt-4o-mini
# XAI_API_KEY → OPENAI_API_KEY
```

## 💡 Tips

- **API Costs**: Monitor your usage at https://console.x.ai/
- **Rate Limits**: Grok has rate limits - check xAI documentation
- **Model Options**: You can also use `grok-2` or other Grok models

## 🆘 Troubleshooting

**"XAI_API_KEY not found"**
- Make sure `.env` file exists in project root
- Check that you've added `XAI_API_KEY=your-key` (no spaces around `=`)
- Verify the virtual environment is activated

**"Authentication Error"**
- Verify your API key is correct
- Check that it starts with `xai-`
- Ensure you have credits/access on your xAI account

**"Model not found"**
- Try using `grok-beta` (default)
- Check xAI documentation for available models

## 📚 Resources

- [xAI Console](https://console.x.ai/)
- [xAI Documentation](https://docs.x.ai/)
- [LangChain xAI Integration](https://python.langchain.com/docs/integrations/chat/xai/)

Happy learning with Grok! 🚀
