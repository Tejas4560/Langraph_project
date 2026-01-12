import { useState } from 'react'
import axios from 'axios'

const Example3 = () => {
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
            const response = await axios.post('/api/example3', { user_input: userInput })
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
                <h2 className="text-3xl font-bold gradient-text mb-2">🔧 Example 3: Tool-Calling Agent</h2>
                <p className="text-gray-600"><strong>Concepts:</strong> Tool Integration, ReAct Pattern</p>
            </div>

            <div className="card p-6 mb-6 bg-blue-50 border border-blue-200">
                <p className="text-blue-800">This agent can use tools to solve problems:</p>
                <ul className="list-disc list-inside mt-2 text-blue-700">
                    <li>🧮 <strong>Calculator</strong> - Solve math problems</li>
                    <li>📝 <strong>Word Counter</strong> - Count words in text</li>
                </ul>
            </div>

            <div className="card p-6">
                <form onSubmit={handleSubmit}>
                    <label className="block mb-2 font-semibold">Ask the agent a question:</label>
                    <input
                        type="text"
                        value={userInput}
                        onChange={(e) => setUserInput(e.target.value)}
                        placeholder="What is 25 * 17 + 42?"
                        className="w-full p-3 border border-gray-300 rounded-lg mb-4"
                        required
                    />
                    <button type="submit" disabled={loading} className="gradient-button text-white px-6 py-3 rounded-lg font-semibold disabled:opacity-50">
                        {loading ? '🔄 Agent thinking...' : '🚀 Run Example 3'}
                    </button>
                </form>

                {error && <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">❌ Error: {error}</div>}

                {result && (
                    <div className="mt-6">
                        <div className="p-4 bg-green-50 border border-green-200 rounded-lg mb-4">
                            <p className="text-green-800 font-semibold">✅ Agent completed the task!</p>
                            <p className="text-sm text-gray-600 mt-1">🔧 Tools used: {result.tool_calls} time(s)</p>
                        </div>
                        <div className="card p-6 bg-gray-50">
                            <h3 className="text-xl font-bold mb-3">🤖 Response:</h3>
                            <p className="text-gray-800 whitespace-pre-wrap">{result.response}</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

export default Example3
