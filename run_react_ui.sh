#!/bin/bash
# Launch script for React + FastAPI Web UI

echo "🚀 Starting LangGraph Learning Hub (React + FastAPI)"
echo ""

# Check if in correct directory
if [ ! -d "web-ui" ]; then
    echo "❌ Error: Please run this script from the Langraph_Project directory"
    exit 1
fi

# Start backend in background
echo "📡 Starting FastAPI backend..."
cd web-ui/backend
python main.py &
BACKEND_PID=$!
cd ../..

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting React frontend..."
cd web-ui/frontend
npm run dev

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
