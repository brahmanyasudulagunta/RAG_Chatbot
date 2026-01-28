import { useState } from 'react'

const API_URL = 'http://localhost:8000/api'

export default function QuizPage() {
    const [topic, setTopic] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const [quiz, setQuiz] = useState(null)
    const [error, setError] = useState(null)

    const handleGenerate = async () => {
        setIsLoading(true)
        setError(null)

        try {
            const response = await fetch(`${API_URL}/quiz/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic: topic.trim() || null })
            })

            if (!response.ok) throw new Error('Failed to generate quiz')

            const data = await response.json()
            setQuiz(data)
        } catch (err) {
            console.error('Error:', err)
            setError('Failed to generate quiz. Please try again.')
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <>
            <header className="page-header">
                <h2>📝 Quiz Agent</h2>
                <p>Generate practice quizzes from your Network Security knowledge base</p>
            </header>

            <div className="quiz-container">
                <div className="quiz-input-section">
                    <h3>Generate a Quiz</h3>
                    <p>Enter a topic or leave blank for a random quiz covering all materials.</p>

                    <div className="topic-input-wrapper">
                        <input
                            type="text"
                            className="topic-input"
                            placeholder="e.g., AES encryption, Firewalls, SSL/TLS..."
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
                            disabled={isLoading}
                        />
                        <button
                            className="generate-btn"
                            onClick={handleGenerate}
                            disabled={isLoading}
                        >
                            {isLoading ? (
                                <div className="loading">
                                    <span className="loading-spinner"></span>
                                    Generating...
                                </div>
                            ) : (
                                '✨ Generate Quiz'
                            )}
                        </button>
                    </div>
                </div>

                {error && (
                    <div className="toast error">
                        {error}
                    </div>
                )}

                {quiz && (
                    <div className="quiz-output">
                        <h3>
                            <span>📋</span>
                            Generated Quiz
                        </h3>
                        <div className="quiz-topic">
                            Topic: <strong>{quiz.topic}</strong>
                        </div>

                        <div className="quiz-content">
                            {quiz.quiz_text}
                        </div>

                        {quiz.sources && quiz.sources.length > 0 && (
                            <div className="quiz-sources">
                                <strong>Sources:</strong> {quiz.sources.join(', ')}
                            </div>
                        )}
                    </div>
                )}

                {!quiz && !isLoading && (
                    <div className="empty-state" style={{ marginTop: '48px' }}>
                        <div className="icon">📚</div>
                        <h3>Ready to Test Your Knowledge?</h3>
                        <p>Generate a quiz to practice network security concepts with mixed question types including True/False, MCQs, and open-ended questions.</p>
                    </div>
                )}
            </div>
        </>
    )
}
