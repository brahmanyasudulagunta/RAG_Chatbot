import { useState, useRef, useEffect } from 'react'
import ChatMessage, { TypingIndicator } from '../components/ChatMessage'

const API_URL = 'http://localhost:8000/api'

export default function TutorPage({ chat, updateMessages }) {
    const [input, setInput] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [chat.messages, isLoading])

    const handleSend = async () => {
        if (!input.trim() || isLoading) return

        const userMessage = input.trim()
        setInput('')

        const newMessages = [...chat.messages, { user: userMessage, bot: null }]
        updateMessages(newMessages)
        setIsLoading(true)

        try {
            const response = await fetch(`${API_URL}/tutor/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage, chat_id: chat.id })
            })

            if (!response.ok) throw new Error('Failed to get response')

            const data = await response.json()

            updateMessages([
                ...chat.messages,
                { user: userMessage, bot: data.response }
            ])
        } catch (error) {
            console.error('Error:', error)
            updateMessages([
                ...chat.messages,
                { user: userMessage, bot: 'Sorry, I encountered an error. Please try again.' }
            ])
        } finally {
            setIsLoading(false)
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    return (
        <>
            <header className="page-header">
                <h2>💬 Tutor Agent</h2>
                <p>Ask questions about Network Security - powered by RAG</p>
            </header>

            <div className="chat-container">
                {chat.messages.length === 0 ? (
                    <div className="empty-state">
                        <div className="icon">🎓</div>
                        <h3>Start a Conversation</h3>
                        <p>Ask me anything about network security, cryptography, or cybersecurity concepts!</p>
                    </div>
                ) : (
                    chat.messages.map((msg, idx) => (
                        <div key={idx}>
                            <ChatMessage message={msg.user} type="user" />
                            {msg.bot ? (
                                <ChatMessage message={msg.bot} type="bot" />
                            ) : isLoading && idx === chat.messages.length - 1 ? (
                                <TypingIndicator />
                            ) : null}
                        </div>
                    ))
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="chat-input-container">
                <div className="chat-input-wrapper">
                    <input
                        type="text"
                        className="chat-input"
                        placeholder="Ask about network security, cryptography, protocols..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        disabled={isLoading}
                    />
                    <button
                        className="send-btn"
                        onClick={handleSend}
                        disabled={!input.trim() || isLoading}
                    >
                        {isLoading ? (
                            <span className="loading-spinner"></span>
                        ) : (
                            <>Send →</>
                        )}
                    </button>
                </div>
            </div>
        </>
    )
}
