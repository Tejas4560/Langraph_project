import { useState } from 'react'
import axios from 'axios'

const Example4 = () => {
    const [topic, setTopic] = useState('')
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError(null)
        setResult(null)

        try {
            const response = await axios.post('/api/example4', { topic })
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
                <h2 className="text-3xl font-bold gradient-text mb-2">👥 Example 4: Multi-Agent Research Team</h2>
                <p className="text-gray-600"><strong>Concepts:</strong> Multi-Agent Coordination, Specialized Roles</p>
            </div>

            <div className="card p-6 mb-6 bg-blue-50 border border-blue-200">
                <p className="text-blue-800">A team of specialized agents collaborates on research:</p>
                <ul className="list-disc list-inside mt-2 text-blue-700">
                    <li>📋 <strong>Supervisor</strong> - Coordinates the team</li>
                    <li>🔍 <strong>Researcher</strong> - Gathers information</li>
                    <li>📊 <strong>Analyst</strong> - Analyzes findings</li>
                    <li>✍️ <strong>Writer</strong> - Creates the report</li>
                </ul>
            </div>

            <div className="card p-6">
                <form onSubmit={handleSubmit}>
                    <label className="block mb-2 font-semibold">Enter a research topic:</label>
                    <input
                        type="text"
                        value={topic}
                        onChange={(e) => setTopic(e.target.value)}
                        placeholder="What is LangGraph and how does it work?"
                        className="w-full p-3 border border-gray-300 rounded-lg mb-4"
                        required
                    />
                    <button type="submit" disabled={loading} className="gradient-button text-white px-6 py-3 rounded-lg font-semibold disabled:opacity-50">
                        {loading ? '🔄 Research team collaborating...' : '🚀 Run Example 4'}
                    </button>
                </form>

                {error && <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">❌ Error: {error}</div>}

                {result && (
                    <div className="mt-6">
                        <div className="p-4 bg-green-50 border border-green-200 rounded-lg mb-4">
                            <p className="text-green-800 font-semibold">✅ Research complete!</p>
                        </div>
                        <div className="card p-6 bg-gray-50">
                            <h3 className="text-xl font-bold mb-3">📄 Final Report:</h3>
                            <div className="prose max-w-none text-gray-800 whitespace-pre-wrap">{result.final_report}</div>
                        </div>
                        <details className="mt-4 card p-4">
                            <summary className="cursor-pointer font-semibold">📊 Team Statistics</summary>
                            <div className="mt-2 space-y-1 text-sm">
                                <p><strong>Iterations:</strong> {result.iterations}</p>
                                <p><strong>Research Length:</strong> {result.research_length} characters</p>
                                <p><strong>Analysis Length:</strong> {result.analysis_length} characters</p>
                            </div>
                        </details>
                    </div>
                )}
            </div>
        </div>
    )
}

export default Example4
