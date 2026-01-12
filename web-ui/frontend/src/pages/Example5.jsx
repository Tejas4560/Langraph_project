import { useState } from 'react'
import axios from 'axios'

const Example5 = () => {
    const [topic, setTopic] = useState('')
    const [draft, setDraft] = useState(null)
    const [feedback, setFeedback] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const generateDraft = async (withFeedback = false) => {
        setLoading(true)
        setError(null)

        try {
            const response = await axios.post('/api/example5', {
                topic,
                feedback: withFeedback ? feedback : null
            })

            if (response.data.success) {
                setDraft(response.data.data.draft)
                if (withFeedback) setFeedback('')
            } else {
                setError(response.data.error)
            }
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const handleStart = (e) => {
        e.preventDefault()
        generateDraft(false)
    }

    const handleRevise = () => {
        if (feedback.trim()) {
            generateDraft(true)
        }
    }

    return (
        <div className="max-w-4xl mx-auto">
            <div className="card p-6 mb-6">
                <h2 className="text-3xl font-bold gradient-text mb-2">✋ Example 5: Human-in-the-Loop Workflow</h2>
                <p className="text-gray-600"><strong>Concepts:</strong> Interrupts, Approval Workflows, Persistence</p>
            </div>

            <div className="card p-6 mb-6 bg-blue-50 border border-blue-200">
                <p className="text-blue-800">This workflow demonstrates human oversight:</p>
                <ol className="list-decimal list-inside mt-2 text-blue-700">
                    <li>Agent drafts content</li>
                    <li>You review and approve/reject</li>
                    <li>If rejected, agent revises based on feedback</li>
                    <li>Loop continues until approved</li>
                </ol>
            </div>

            <div className="card p-6">
                {!draft ? (
                    <form onSubmit={handleStart}>
                        <label className="block mb-2 font-semibold">Enter a content topic:</label>
                        <input
                            type="text"
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            placeholder="The Benefits of Learning LangGraph"
                            className="w-full p-3 border border-gray-300 rounded-lg mb-4"
                            required
                        />
                        <button type="submit" disabled={loading} className="gradient-button text-white px-6 py-3 rounded-lg font-semibold disabled:opacity-50">
                            {loading ? '🔄 Generating...' : '🚀 Start Workflow'}
                        </button>
                    </form>
                ) : (
                    <div>
                        <div className="card p-6 bg-gray-50 mb-4">
                            <h3 className="text-xl font-bold mb-3">📝 Draft Content:</h3>
                            <p className="text-gray-800 whitespace-pre-wrap">{draft}</p>
                        </div>

                        <div className="grid grid-cols-2 gap-4 mb-4">
                            <button
                                onClick={() => {
                                    alert('🎉 Content approved and published!')
                                    setDraft(null)
                                    setTopic('')
                                }}
                                className="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-semibold"
                            >
                                ✅ Approve
                            </button>
                            <button
                                onClick={() => document.getElementById('feedback-section').classList.toggle('hidden')}
                                className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold"
                            >
                                ❌ Request Revision
                            </button>
                        </div>

                        <div id="feedback-section" className="hidden">
                            <label className="block mb-2 font-semibold">Provide feedback for revision:</label>
                            <textarea
                                value={feedback}
                                onChange={(e) => setFeedback(e.target.value)}
                                placeholder="Please make it more engaging and add specific examples..."
                                className="w-full p-3 border border-gray-300 rounded-lg mb-2 h-24"
                            />
                            <button
                                onClick={handleRevise}
                                disabled={loading || !feedback.trim()}
                                className="gradient-button text-white px-6 py-3 rounded-lg font-semibold disabled:opacity-50"
                            >
                                {loading ? '🔄 Revising...' : '📝 Submit Feedback'}
                            </button>
                        </div>
                    </div>
                )}

                {error && <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">❌ Error: {error}</div>}
            </div>
        </div>
    )
}

export default Example5
