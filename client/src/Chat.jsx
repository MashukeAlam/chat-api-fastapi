// src/Chat.jsx

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios'; // Add axios for HTTP requests
import './Chat.css'; // Add any styling you like

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [username, setUsername] = useState(''); // Add a field to set username
  const [receiver, setReceiver] = useState('');
  const socketRef = useRef(null);

    // Fetch chat history when the component mounts or when username or receiver changes
    useEffect(() => {
      if (username && receiver) {
        axios.get(`/api/messages/${username}/${receiver}`)
          .then(response => {
            setMessages(response.data.messages);
          })
          .catch(error => {
            console.error("There was an error fetching the chat history!", error);
          });
      }
    }, [username, receiver]);

  useEffect(() => {
    // Initialize WebSocket connection
    socketRef.current = new WebSocket(`ws://localhost:8000/ws/chat/${username}`);

    socketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log(data);
      
      setMessages((prevMessages) => [...prevMessages, data]);
    };

    socketRef.current.onopen = () => {
      console.log('WebSocket connection established');
    };

    socketRef.current.onclose = () => {
      console.log('WebSocket connection closed');
    };

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [username]);

  const sendMessage = () => {
    if (input.trim() && username && receiver) {
      const message = JSON.stringify({
        receiver: receiver,
        sender: username,
        content: input,
      });
      socketRef.current.send(message);
      setMessages((prevMessages) => [...prevMessages, JSON.parse(message)]);
      setInput('');
    } else {
      alert('Please fill in all fields.');
    }
  };

  return (
    <div>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className="message">
            <strong>{msg.sender}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <div className="input-group">
        <input
          type="text"
          placeholder="Your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="text"
          placeholder="Receiver username"
          value={receiver}
          onChange={(e) => setReceiver(e.target.value)}
        />
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
