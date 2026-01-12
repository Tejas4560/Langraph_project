const Home = () => {
    return (
        <div className="max-w-6xl mx-auto">
            <div className="card p-8 mb-6">
                <h2 className="text-3xl font-bold gradient-text mb-4">
                    Welcome to the LangGraph Learning Hub! 👋
                </h2>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
                <div className="card p-6">
                    <h3 className="text-2xl font-bold mb-4">🎯 What You'll Learn</h3>
                    <p className="mb-4">This project teaches you LangGraph through 5 progressive examples:</p>
                    <ol className="list-decimal list-inside space-y-2 text-gray-700">
                        <li><strong>Basic Chatbot</strong> - Nodes, edges, state management</li>
                        <li><strong>Sentiment Router</strong> - Conditional routing</li>
                        <li><strong>Tool-Calling Agent</strong> - ReAct pattern with tools</li>
                        <li><strong>Multi-Agent System</strong> - Agent coordination</li>
                        <li><strong>Human-in-the-Loop</strong> - Approval workflows</li>
                    </ol>
                    <p className="mt-4 text-purple-600 font-semibold">
                        Plus a complete AI Research Assistant combining everything!
                    </p>
                </div>

                <div className="card p-6">
                    <h3 className="text-2xl font-bold mb-4">🚀 Getting Started</h3>
                    <ol className="list-decimal list-inside space-y-3 text-gray-700">
                        <li>Select an example from the sidebar</li>
                        <li>Enter your input or question</li>
                        <li>Click "Run" to see LangGraph in action</li>
                        <li>Observe the graph execution flow</li>
                        <li>Learn from the results!</li>
                    </ol>
                    <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                        <p className="text-green-800 font-semibold">✅ All systems ready!</p>
                    </div>
                </div>
            </div>

            <div className="card p-6 mt-6 gradient-bg text-white">
                <p className="text-xl text-center">
                    👈 Select an example from the sidebar to get started!
                </p>
            </div>
        </div>
    )
}

export default Home
