import { Link, useLocation } from 'react-router-dom'

const Sidebar = () => {
    const location = useLocation()

    const menuItems = [
        { path: '/', label: '🏠 Home', icon: '🏠' },
        { path: '/example1', label: '💬 Example 1: Basic Chatbot', icon: '💬' },
        { path: '/example2', label: '🎭 Example 2: Sentiment Router', icon: '🎭' },
        { path: '/example3', label: '🔧 Example 3: Tool-Calling Agent', icon: '🔧' },
        { path: '/example4', label: '👥 Example 4: Multi-Agent System', icon: '👥' },
        { path: '/example5', label: '✋ Example 5: Human-in-the-Loop', icon: '✋' },
        { path: '/final-project', label: '🎯 Final Project', icon: '🎯' },
    ]

    return (
        <div className="w-64 gradient-bg min-h-screen text-white p-6">
            <h2 className="text-2xl font-bold mb-8">📚 Navigation</h2>
            <nav>
                <ul className="space-y-2">
                    {menuItems.map((item) => (
                        <li key={item.path}>
                            <Link
                                to={item.path}
                                className={`block px-4 py-3 rounded-lg transition-all ${location.pathname === item.path
                                        ? 'bg-white bg-opacity-20 font-semibold'
                                        : 'hover:bg-white hover:bg-opacity-10'
                                    }`}
                            >
                                {item.label}
                            </Link>
                        </li>
                    ))}
                </ul>
            </nav>
            <div className="mt-8 p-4 bg-white bg-opacity-10 rounded-lg">
                <h3 className="font-bold mb-2">🎓 About</h3>
                <p className="text-sm opacity-90">
                    Interactive UI for testing LangGraph examples.
                </p>
                <p className="text-xs mt-2 opacity-75">
                    Powered by React, FastAPI & Groq
                </p>
            </div>
        </div>
    )
}

export default Sidebar
