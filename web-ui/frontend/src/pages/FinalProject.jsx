import { useState } from 'react'
import axios from 'axios'

const FinalProject = () => {
    const [question, setQuestion] = useState('')
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError(null)
        setResult(null)

        try {
            const response = await axios.post('/api/final-project', { question })
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
                <h2 className="text-3xl font-bold gradient-text mb-2">🎯 AI Research Assistant</h2>
                <p className="text-gray-600"><strong>Combines All Concepts:</strong> Complete Production-Ready Application</p>
            </div>

            <div className="card p-6 mb-6 bg-blue-50 border border-blue-200">
                <p className="text-blue-800">This combines everything you've learned:</p>
                <ul className="list-disc list-inside mt-2 text-blue-700">
                    <li>✅ Task classification (simple vs complex)</li>
                    <li>✅ Multi-agent collaboration</li>
                    <li>✅ Tool integration</li>
                    <li>✅ Conditional routing</li>
                </ul>
            </div>

            <div className="card p-6">
                <form onSubmit={handleSubmit}>
                    <label className="block mb-2 font-semibold">Ask the research assistant:</label>
                    <textarea
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        placeholder="How can LangGraph be used to build production AI applications?"
                        className="w-full p-3 border border-gray-300 rounded-lg mb-4 h-32"
                        required
                    />
                    <button type="submit" disabled={loading} className="gradient-button text-white px-6 py-3 rounded-lg font-semibold disabled:opacity-50">
                        {loading ? '🔄 Research assistant working...' : '🚀 Run Research Assistant'}
                    </button>
                </form>

                {error && <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">❌ Error: {error}</div>}

                {result && (
                    <div className="mt-6">
                        <div className="p-4 bg-green-50 border border-green-200 rounded-lg mb-4">
                            <p className="text-green-800 font-semibold">✅ Research complete!</p>
                            <p className="text-sm text-gray-600 mt-1">
                                <strong>Task Classification:</strong> {result.complexity === 'complex' ? '🔴 Complex' : '🟢 Simple'}
                            </p>
                        </div>
                        <div className="card p-6 bg-gray-50">
                            <h3 className="text-xl font-bold mb-3">📄 Research Report:</h3>
                            <div className="prose max-w-none text-gray-800 whitespace-pre-wrap">{result.final_report}</div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

export default FinalProject
