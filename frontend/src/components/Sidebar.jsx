export default function Sidebar({
    activePage,
    setActivePage,
    chats,
    activeChat,
    setActiveChat,
    onNewChat,
    onDeleteChat
}) {
    return (
        <aside className="sidebar">
            <div className="sidebar-header">
                <div className="logo">🛡️</div>
                <div className="brand">
                    <h1>SecureBot</h1>
                    <span>Network Security Tutor</span>
                </div>
            </div>

            <nav className="nav-section">
                <div className="nav-label">Agents</div>
                <div
                    className={`nav-item ${activePage === 'tutor' ? 'active' : ''}`}
                    onClick={() => setActivePage('tutor')}
                >
                    <span className="icon">💬</span>
                    <span>Tutor Agent</span>
                </div>
                <div
                    className={`nav-item ${activePage === 'quiz' ? 'active' : ''}`}
                    onClick={() => setActivePage('quiz')}
                >
                    <span className="icon">📝</span>
                    <span>Quiz Agent</span>
                </div>
            </nav>

            {activePage === 'tutor' && (
                <div className="nav-section">
                    <div className="nav-label">Conversations</div>
                    <button className="new-chat-btn" onClick={onNewChat}>
                        <span>+</span>
                        <span>New Chat</span>
                    </button>
                    <div className="chat-list">
                        {chats.map((chat, idx) => (
                            <div
                                key={chat.id}
                                className={`chat-item ${activeChat === chat.id ? 'active' : ''}`}
                                onClick={() => setActiveChat(chat.id)}
                            >
                                <span>Chat {idx + 1}</span>
                                <button
                                    className="delete-btn"
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        onDeleteChat(chat.id)
                                    }}
                                >
                                    🗑️
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </aside>
    )
}
