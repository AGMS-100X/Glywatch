import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './ChatPage.css';

export default function ChatPage() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: 'Is everyone available for a call this evening?',
      sender: 'them',
      timestamp: '2:00 PM'
    },
    {
      id: 2,
      text: 'Yes, that works for me.',
      sender: 'me',
      timestamp: '2:01 PM'
    },
    {
      id: 3,
      text: 'Sure, what time?',
      sender: 'them',
      timestamp: '2:02 PM'
    }
  ]);
  const [newMessage, setNewMessage] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleBack = () => {
    navigate(-1);
  };

  const handleSendMessage = () => {
    if (newMessage.trim()) {
      const message = {
        id: Date.now(),
        text: newMessage,
        sender: 'me',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages([...messages, message]);
      setNewMessage('');
      
      // Send message to backend
      fetch('/api/chat/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: newMessage,
          timestamp: new Date().toISOString()
        })
      }).catch(error => {
        console.error('Error sending message:', error);
      });
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  const handleVoiceMessage = () => {
    // Voice message functionality
    alert('Voice message functionality');
  };

  return (
    <div className="chat-page">
      {/* Header */}
      <div className="chat-header">
        <button className="back-button" onClick={handleBack}>
          ←
        </button>
        <h1>Chat</h1>
      </div>

      {/* Messages Container */}
      <div className="messages-container">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.sender}`}>
            <div className="message-bubble">
              <div className="message-text">{message.text}</div>
              <div className="message-timestamp">{message.timestamp}</div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Section */}
      <div className="chat-input-section">
        <div className="input-container">
          <input
            type="text"
            placeholder="Message"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            className="message-input"
          />
          <button 
            className="voice-button"
            onClick={handleVoiceMessage}
          >
            🎤
          </button>
        </div>
      </div>
    </div>
  );
} 