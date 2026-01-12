# 🚀 LangGraph Learning Hub - React UI

A modern React-based web interface for learning LangGraph with interactive examples.

## 🎯 Project Overview

This project provides a hands-on learning environment for LangGraph through 5 progressive examples and a complete AI Research Assistant, all accessible through a beautiful React web interface.

## 📁 Project Structure

```
Langraph_Project/
├── examples/                    # 5 Progressive LangGraph examples
│   ├── 01_basic_chatbot/
│   ├── 02_conditional_routing/
│   ├── 03_tool_calling_agent/
│   ├── 04_multi_agent_system/
│   └── 05_human_in_loop/
├── final_project/               # Complete AI Research Assistant
├── web-ui/                      # React + FastAPI Web Interface
│   ├── backend/                 # FastAPI server
│   └── frontend/                # React application
├── .env                         # Environment variables (GROQ_API_KEY)
└── requirements.txt             # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies (in virtual environment)
pip install -r requirements.txt

# Install backend dependencies
cd web-ui/backend
pip install -r requirements.txt
cd ../..

# Install frontend dependencies
cd web-ui/frontend
npm install
cd ../..
```

### 2. Configure Environment

Create a `.env` file with your Groq API key:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at: https://console.groq.com/

### 3. Launch the Application

**Option 1: Use the launch script**
```bash
./run_react_ui.sh
```

**Option 2: Manual launch (2 terminals)**

Terminal 1 - Backend:
```bash
cd web-ui/backend
python main.py
```

Terminal 2 - Frontend:
```bash
cd web-ui/frontend
npm run dev
```

### 4. Access the Application

- **React UI**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## 📚 Learning Path

### Progressive Examples

1. **Basic Chatbot** (`01_basic_chatbot`)
   - Learn: Nodes, edges, state management
   - Concepts: Linear graphs, TypedDict state

2. **Sentiment Router** (`02_conditional_routing`)
   - Learn: Conditional routing, dynamic flow
   - Concepts: Routing functions, conditional edges

3. **Tool-Calling Agent** (`03_tool_calling_agent`)
   - Learn: Tool integration, ReAct pattern
   - Concepts: LangChain tools, agent loops

4. **Multi-Agent System** (`04_multi_agent_system`)
   - Learn: Agent coordination, specialized roles
   - Concepts: Supervisor pattern, agent collaboration

5. **Human-in-the-Loop** (`05_human_in_loop`)
   - Learn: Approval workflows, interrupts
   - Concepts: Human oversight, revision loops

### Final Project

**AI Research Assistant** (`final_project`)
- Combines all concepts
- Task classification
- Multi-agent workflow
- Production-ready architecture

## 🎨 Web UI Features

- ✅ Beautiful purple gradient design
- ✅ Responsive layout
- ✅ Interactive examples
- ✅ Real-time feedback
- ✅ Error handling
- ✅ Loading states
- ✅ API integration

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangGraph** - Agent orchestration
- **Groq** - Fast LLM inference
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client

## 📖 Documentation

- `web-ui/README.md` - Web UI specific documentation
- `GROQ_SETUP.md` - Groq API configuration guide
- Each example has its own README with detailed explanations

## 🔧 Development

### Running Examples via CLI

You can also run examples directly from the command line:

```bash
python examples/01_basic_chatbot/simple_chain.py
python examples/02_conditional_routing/sentiment_router.py
# ... etc
```

### API Endpoints

The FastAPI backend provides these endpoints:

- `POST /api/example1` - Basic Chatbot
- `POST /api/example2` - Sentiment Router
- `POST /api/example3` - Tool-Calling Agent
- `POST /api/example4` - Multi-Agent System
- `POST /api/example5` - Human-in-the-Loop
- `POST /api/final-project` - AI Research Assistant

See http://localhost:8000/docs for interactive API documentation.

## 🎓 Learning Objectives

By completing this project, you will learn:

- ✅ LangGraph fundamentals (nodes, edges, state)
- ✅ Conditional routing and dynamic flows
- ✅ Tool integration with agents
- ✅ Multi-agent system architecture
- ✅ Human-in-the-loop patterns
- ✅ Production-ready AI application design

## 🤝 Contributing

This is a learning project. Feel free to:
- Experiment with the code
- Add new examples
- Modify the UI
- Extend functionality

## 📝 License

This project is for educational purposes.

## 🎉 Enjoy Learning LangGraph!

Happy coding! 🚀
