import { useState } from 'react'
import axios from 'axios'

const Example1 = () => {
    const [userInput, setUserInput] = useState('')
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError(null)
        setResult(null)

        try {
            const response = await axios.post('/api/example1', {
                user_input: userInput
            })

            if (response.data.success) {
                setResult(response.data.data)
            } else {
                setError(response.data.error)
            }
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="max-w-4xl mx-auto">
            <div className="card p-6 mb-6">
                <h2 className="text-3xl font-bold gradient-text mb-2">💬 Example 1: Basic Chatbot</h2>
                <p className="text-gray-600"><strong>Concepts:</strong> Nodes, Edges, State Management</p>
            </div>

            <div className="card p-6 mb-6 bg-blue-50 border border-blue-200">
                <p className="text-blue-800">
                    This example demonstrates a simple linear graph with three nodes:
                </p>
                <ol className="list-decimal list-inside mt-2 text-blue-700">
                    <li><strong>greet_user</strong> - Initialize the conversation</li>
                    <li><strong>process_message</strong> - Call the LLM</li>
                    <li><strong>format_response</strong> - Format the output</li>
                </ol>
            </div>

            <div className="card p-6">
                <form onSubmit={handleSubmit}>
                    <label className="block mb-2 font-semibold">Enter your message:</label>
                    <input
                        type="text"
                        value={userInput}
                        onChange={(e) => setUserInput(e.target.value)}
                        placeholder="Hello! Can you explain what LangGraph is?"
                        className="w-full p-3 border border-gray-300 rounded-lg mb-4"
                        required
                    />
                    <button
                        type="submit"
                        disabled={loading}
                        className="gradient-button text-white px-6 py-3 rounded-lg font-semibold disabled:opacity-50"
                    >
                        {loading ? '🔄 Processing...' : '🚀 Run Example 1'}
                    </button>
                </form>

                {error && (
                    <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">
                        ❌ Error: {error}
                    </div>
                )}

                {result && (
                    <div className="mt-6">
                        <div className="p-4 bg-green-50 border border-green-200 rounded-lg mb-4">
                            <p className="text-green-800 font-semibold">✅ Graph execution complete!</p>
                        </div>

                        <div className="card p-6 bg-gray-50">
                            <h3 className="text-xl font-bold mb-3">🤖 Response:</h3>
                            <p className="text-gray-800 whitespace-pre-wrap">{result.response}</p>
                        </div>

                        {result.metadata && (
                            <details className="mt-4 card p-4">
                                <summary className="cursor-pointer font-semibold">📊 View Execution Metadata</summary>
                                <pre className="mt-2 p-4 bg-gray-100 rounded overflow-auto text-sm">
                                    {JSON.stringify(result.metadata, null, 2)}
                                </pre>
                            </details>
                        )}
                    </div>
                )}
            </div>
        </div>
    )
}

export default Example1
