// src/App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Mock response for demonstration
    setResponse(`You asked: "${input}". This is a mock response.`);
    setInput('');
  };

  return (
    <div className="App">
      <h1>What can I help with?</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question..."
          required
        />
        <button type="submit">Send</button>
      </form>
      <div className="response">
        {response && <p>{response}</p>}
      </div>
    </div>
  );
}

export default App;
