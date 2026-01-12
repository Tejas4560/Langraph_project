#!/bin/bash
# Script to update all examples to use Groq instead of xAI

echo "🔄 Updating all examples to use Groq..."

# Update Example 1
sed -i 's/from langchain_xai import ChatXAI/from langchain_groq import ChatGroq/g' examples/01_basic_chatbot/simple_chain.py
sed -i 's/ChatXAI(/ChatGroq(/g' examples/01_basic_chatbot/simple_chain.py
sed -i 's/model="grok-beta"/model="llama-3.3-70b-versatile"/g' examples/01_basic_chatbot/simple_chain.py
sed -i 's/XAI_API_KEY/GROQ_API_KEY/g' examples/01_basic_chatbot/simple_chain.py
sed -i 's/xAI Grok/Groq/g' examples/01_basic_chatbot/simple_chain.py
sed -i 's/https:\/\/console.x.ai\//https:\/\/console.groq.com\//g' examples/01_basic_chatbot/simple_chain.py

# Update Example 2
sed -i 's/from langchain_xai import ChatXAI/from langchain_groq import ChatGroq/g' examples/02_conditional_routing/sentiment_router.py
sed -i 's/ChatXAI(/ChatGroq(/g' examples/02_conditional_routing/sentiment_router.py
sed -i 's/model="grok-beta"/model="llama-3.3-70b-versatile"/g' examples/02_conditional_routing/sentiment_router.py
sed -i 's/XAI_API_KEY/GROQ_API_KEY/g' examples/02_conditional_routing/sentiment_router.py

# Update Example 3
sed -i 's/from langchain_xai import ChatXAI/from langchain_groq import ChatGroq/g' examples/03_tool_calling_agent/calculator_agent.py
sed -i 's/ChatXAI(/ChatGroq(/g' examples/03_tool_calling_agent/calculator_agent.py
sed -i 's/model="grok-beta"/model="llama-3.3-70b-versatile"/g' examples/03_tool_calling_agent/calculator_agent.py
sed -i 's/XAI_API_KEY/GROQ_API_KEY/g' examples/03_tool_calling_agent/calculator_agent.py

# Update Example 4
sed -i 's/from langchain_xai import ChatXAI/from langchain_groq import ChatGroq/g' examples/04_multi_agent_system/research_team.py
sed -i 's/ChatXAI(/ChatGroq(/g' examples/04_multi_agent_system/research_team.py
sed -i 's/model="grok-beta"/model="llama-3.3-70b-versatile"/g' examples/04_multi_agent_system/research_team.py
sed -i 's/XAI_API_KEY/GROQ_API_KEY/g' examples/04_multi_agent_system/research_team.py

# Update Example 5
sed -i 's/from langchain_xai import ChatXAI/from langchain_groq import ChatGroq/g' examples/05_human_in_loop/approval_workflow.py
sed -i 's/ChatXAI(/ChatGroq(/g' examples/05_human_in_loop/approval_workflow.py
sed -i 's/model="grok-beta"/model="llama-3.3-70b-versatile"/g' examples/05_human_in_loop/approval_workflow.py
sed -i 's/XAI_API_KEY/GROQ_API_KEY/g' examples/05_human_in_loop/approval_workflow.py

# Update Final Project
sed -i 's/from langchain_xai import ChatXAI/from langchain_groq import ChatGroq/g' final_project/ai_research_assistant.py
sed -i 's/ChatXAI(/ChatGroq(/g' final_project/ai_research_assistant.py
sed -i 's/model="grok-beta"/model="llama-3.3-70b-versatile"/g' final_project/ai_research_assistant.py
sed -i 's/XAI_API_KEY/GROQ_API_KEY/g' final_project/ai_research_assistant.py

echo "✅ All examples updated to use Groq!"
echo ""
echo "📝 Next steps:"
echo "1. Add your Groq API key to .env file: GROQ_API_KEY=your_key_here"
echo "2. Run the examples!"
