import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import AskQuestion from './components/AskQuestion';
import SubmitRequest from './components/SubmitRequest';
import Admin from './components/Admin';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="app-header">
          <div className="header-content">
            <h1>🏘️ The Vistas At Gallahan, HOA</h1>
            <p>Your guide to understanding HOA rules and submitting requests</p>
          </div>
          <nav className="nav-menu">
            <Link to="/" className="nav-link">Ask Questions</Link>
            <Link to="/submit-request" className="nav-link">Submit Request</Link>
          </nav>
        </header>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<AskQuestion />} />
            <Route path="/submit-request" element={<SubmitRequest />} />
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </main>

        <footer className="app-footer">
          <p>© 2026 The Vistas At Gallahan, HOA - Helping homeowners navigate HOA regulations</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
