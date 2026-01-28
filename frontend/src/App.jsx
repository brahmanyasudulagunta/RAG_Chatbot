import { useState } from 'react'
import Sidebar from './components/Sidebar'
import TutorPage from './pages/TutorPage'
import QuizPage from './pages/QuizPage'
import './index.css'

function App() {
  const [activePage, setActivePage] = useState('tutor')
  const [chats, setChats] = useState([{ id: '1', messages: [] }])
  const [activeChat, setActiveChat] = useState('1')

  const handleNewChat = () => {
    const newId = String(Date.now())
    setChats([...chats, { id: newId, messages: [] }])
    setActiveChat(newId)
  }

  const handleDeleteChat = (chatId) => {
    if (chats.length <= 1) return
    const newChats = chats.filter(c => c.id !== chatId)
    setChats(newChats)
    if (activeChat === chatId) {
      setActiveChat(newChats[0].id)
    }
  }

  const updateChatMessages = (chatId, messages) => {
    setChats(chats.map(c => c.id === chatId ? { ...c, messages } : c))
  }

  const currentChat = chats.find(c => c.id === activeChat) || chats[0]

  return (
    <div className="app">
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
        chats={chats}
        activeChat={activeChat}
        setActiveChat={setActiveChat}
        onNewChat={handleNewChat}
        onDeleteChat={handleDeleteChat}
      />
      <main className="main-content">
        {activePage === 'tutor' ? (
          <TutorPage
            chat={currentChat}
            updateMessages={(msgs) => updateChatMessages(currentChat.id, msgs)}
          />
        ) : (
          <QuizPage />
        )}
      </main>
    </div>
  )
}

export default App
