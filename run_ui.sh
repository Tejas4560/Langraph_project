#!/bin/bash
# Launch script for LangGraph Web UI

echo "🚀 Starting LangGraph Learning Hub..."
echo ""
echo "📝 Make sure your GROQ_API_KEY is set in .env file"
echo ""

# Activate virtual environment
source venv/bin/activate

# Run Streamlit app
streamlit run app.py --server.port 8501 --server.headless true
