export default function ChatMessage({ message, type }) {
    return (
        <div className={`message ${type}`}>
            <div className="message-avatar">
                {type === 'bot' ? '🤖' : '👤'}
            </div>
            <div className="message-content">
                {message.split('\n').map((line, idx) => (
                    <p key={idx}>{line || '\u00A0'}</p>
                ))}
            </div>
        </div>
    )
}

export function TypingIndicator() {
    return (
        <div className="message bot">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
                <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    )
}
