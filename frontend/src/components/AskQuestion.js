import React, { useState } from 'react';
import axios from 'axios';
import './AskQuestion.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function AskQuestion() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const exampleQuestions = [
    "Can I paint my house a different color?",
    "What are the rules about parking on the street?",
    "Am I allowed to install solar panels?",
    "What are the quiet hours in the community?",
    "Can I have a home business?"
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError('');
    setAnswer(null);

    try {
      const response = await axios.post(`${API_URL}/api/ask`, {
        question: question
      });
      setAnswer(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (exampleQuestion) => {
    setQuestion(exampleQuestion);
  };

  return (
    <div className="ask-question-container">
      <div className="question-card">
        <h2>Ask About HOA Bylaws</h2>
        <p className="subtitle">Get instant answers to your HOA questions</p>

        <div className="example-questions">
          <h3>Example Questions:</h3>
          <div className="example-list">
            {exampleQuestions.map((eq, index) => (
              <button
                key={index}
                className="example-btn"
                onClick={() => handleExampleClick(eq)}
              >
                {eq}
              </button>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="question-form">
          <textarea
            className="question-input"
            placeholder="Type your question here... (e.g., Can I install a fence?)"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            rows="4"
          />
          <button 
            type="submit" 
            className="submit-btn"
            disabled={loading || !question.trim()}
          >
            {loading ? 'Searching...' : 'Ask Question'}
          </button>
        </form>

        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}

        {answer && (
          <div className="answer-section">
            <h3>Answer:</h3>
            <div className="answer-content">
              <p>{answer.answer}</p>
            </div>
            {answer.sources && answer.sources.length > 0 && (
              <div className="sources">
                <h4>Sources:</h4>
                <ul>
                  {answer.sources.map((source, index) => (
                    <li key={index}>{source}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default AskQuestion;
