#!/bin/bash
# Script to update all examples to use Grok (xAI) instead of OpenAI

echo "🔄 Updating all examples to use xAI Grok..."

# Update Example 2
sed -i 's/from langchain_openai import ChatOpenAI/from langchain_xai import ChatXAI/g' examples/02_conditional_routing/sentiment_router.py
sed -i 's/ChatOpenAI(/ChatXAI(/g' examples/02_conditional_routing/sentiment_router.py
sed -i 's/model="gpt-4o-mini"/model="grok-beta"/g' examples/02_conditional_routing/sentiment_router.py
sed -i 's/OPENAI_API_KEY/XAI_API_KEY/g' examples/02_conditional_routing/sentiment_router.py

# Update Example 3
sed -i 's/from langchain_openai import ChatOpenAI/from langchain_xai import ChatXAI/g' examples/03_tool_calling_agent/calculator_agent.py
sed -i 's/ChatOpenAI(/ChatXAI(/g' examples/03_tool_calling_agent/calculator_agent.py
sed -i 's/model="gpt-4o-mini"/model="grok-beta"/g' examples/03_tool_calling_agent/calculator_agent.py
sed -i 's/OPENAI_API_KEY/XAI_API_KEY/g' examples/03_tool_calling_agent/calculator_agent.py

# Update Example 4
sed -i 's/from langchain_openai import ChatOpenAI/from langchain_xai import ChatXAI/g' examples/04_multi_agent_system/research_team.py
sed -i 's/ChatOpenAI(/ChatXAI(/g' examples/04_multi_agent_system/research_team.py
sed -i 's/model="gpt-4o-mini"/model="grok-beta"/g' examples/04_multi_agent_system/research_team.py
sed -i 's/OPENAI_API_KEY/XAI_API_KEY/g' examples/04_multi_agent_system/research_team.py

# Update Example 5
sed -i 's/from langchain_openai import ChatOpenAI/from langchain_xai import ChatXAI/g' examples/05_human_in_loop/approval_workflow.py
sed -i 's/ChatOpenAI(/ChatXAI(/g' examples/05_human_in_loop/approval_workflow.py
sed -i 's/model="gpt-4o-mini"/model="grok-beta"/g' examples/05_human_in_loop/approval_workflow.py
sed -i 's/OPENAI_API_KEY/XAI_API_KEY/g' examples/05_human_in_loop/approval_workflow.py

# Update Final Project
sed -i 's/from langchain_openai import ChatOpenAI/from langchain_xai import ChatXAI/g' final_project/ai_research_assistant.py
sed -i 's/ChatOpenAI(/ChatXAI(/g' final_project/ai_research_assistant.py
sed -i 's/model="gpt-4o-mini"/model="grok-beta"/g' final_project/ai_research_assistant.py
sed -i 's/OPENAI_API_KEY/XAI_API_KEY/g' final_project/ai_research_assistant.py

echo "✅ All examples updated to use xAI Grok!"
echo ""
echo "📝 Next steps:"
echo "1. Get your Grok API key from: https://console.x.ai/"
echo "2. Add it to your .env file: XAI_API_KEY=your_key_here"
echo "3. Run the examples!"
