import { useState } from 'react'
import axios from 'axios'

const Example2 = () => {
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
            const response = await axios.post('/api/example2', {
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

    const getSentimentEmoji = (sentiment) => {
        const emojis = { positive: '😊', negative: '💙', neutral: '🤖' }
        return emojis[sentiment] || '🤖'
    }

    return (
        <div className="max-w-4xl mx-auto">
            <div className="card p-6 mb-6">
                <h2 className="text-3xl font-bold gradient-text mb-2">🎭 Example 2: Sentiment Router</h2>
                <p className="text-gray-600"><strong>Concepts:</strong> Conditional Routing, Dynamic Flow</p>
            </div>

            <div className="card p-6 mb-6 bg-blue-50 border border-blue-200">
                <p className="text-blue-800">
                    This example routes your message to different response nodes based on sentiment:
                </p>
                <ul className="list-disc list-inside mt-2 text-blue-700">
                    <li>😊 <strong>Positive</strong> → Enthusiastic response</li>
                    <li>💙 <strong>Negative</strong> → Empathetic response</li>
                    <li>🤖 <strong>Neutral</strong> → Informative response</li>
                </ul>
            </div>

            <div className="card p-6">
                <form onSubmit={handleSubmit}>
                    <label className="block mb-2 font-semibold">Enter your message:</label>
                    <textarea
                        value={userInput}
                        onChange={(e) => setUserInput(e.target.value)}
                        placeholder="I'm so excited about learning LangGraph!"
                        className="w-full p-3 border border-gray-300 rounded-lg mb-4 h-24"
                        required
                    />
                    <button
                        type="submit"
                        disabled={loading}
                        className="gradient-button text-white px-6 py-3 rounded-lg font-semibold disabled:opacity-50"
                    >
                        {loading ? '🔄 Analyzing...' : '🚀 Run Example 2'}
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
                            <p className="text-green-800 font-semibold">
                                ✅ Detected Sentiment: {getSentimentEmoji(result.sentiment)} {result.sentiment.toUpperCase()}
                            </p>
                            <div className="mt-2 bg-white rounded-full h-2 overflow-hidden">
                                <div
                                    className="gradient-bg h-full transition-all duration-500"
                                    style={{ width: `${result.confidence * 100}%` }}
                                />
                            </div>
                            <p className="text-sm text-gray-600 mt-1">Confidence: {(result.confidence * 100).toFixed(0)}%</p>
                        </div>

                        <div className="card p-6 bg-gray-50">
                            <h3 className="text-xl font-bold mb-3">Response:</h3>
                            <p className="text-gray-800 whitespace-pre-wrap">{result.response}</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

export default Example2
