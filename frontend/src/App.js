import React, { useState } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:5000/get_response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: input }),
      });
      const data = await res.json();
      setResponse(data.answer);
    } catch (error) {
      console.error('Error:', error);
      setResponse('An error occurred with the response.');
    }
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
