import React, { useState } from 'react';
import axios from 'axios';
import './Admin.css';

function Admin() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setMessage('');
    } else {
      setFile(null);
      setMessage('Please select a valid PDF file');
      setMessageType('error');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a PDF file first');
      setMessageType('error');
      return;
    }

    setUploading(true);
    setMessage('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/api/upload-bylaws', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setMessage(`Success! ${response.data.message}`);
      setMessageType('success');
      setFile(null);
      // Clear the file input
      document.getElementById('file-input').value = '';
    } catch (error) {
      setMessage(
        error.response?.data?.detail || 'Error uploading document. Please try again.'
      );
      setMessageType('error');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="admin-container">
      <div className="admin-card">
        <div className="admin-header">
          <h1>🔐 Admin Panel</h1>
          <p>Document Management</p>
        </div>

        <div className="upload-section">
          <h2>Upload HOA Bylaws</h2>
          <p className="upload-description">
            Upload PDF documents to index them for the Q&A system
          </p>

          <div className="file-input-wrapper">
            <input
              type="file"
              id="file-input"
              accept=".pdf"
              onChange={handleFileChange}
              disabled={uploading}
            />
            <label htmlFor="file-input" className="file-input-label">
              {file ? file.name : 'Choose PDF File'}
            </label>
          </div>

          {file && (
            <div className="file-info">
              <span className="file-icon">📄</span>
              <span className="file-name">{file.name}</span>
              <span className="file-size">
                ({(file.size / 1024 / 1024).toFixed(2)} MB)
              </span>
            </div>
          )}

          <button
            onClick={handleUpload}
            disabled={!file || uploading}
            className={`upload-button ${uploading ? 'uploading' : ''}`}
          >
            {uploading ? (
              <>
                <span className="spinner"></span>
                Indexing Document...
              </>
            ) : (
              '📤 Upload & Index'
            )}
          </button>

          {message && (
            <div className={`message ${messageType}`}>
              {messageType === 'success' ? '✅' : '❌'} {message}
            </div>
          )}
        </div>

        <div className="admin-info">
          <h3>ℹ️ Information</h3>
          <ul>
            <li>Only PDF files are supported</li>
            <li>Documents are automatically indexed after upload</li>
            <li>Indexing may take a few moments for large documents</li>
            <li>Multiple documents can be uploaded sequentially</li>
          </ul>
        </div>

        <div className="admin-footer">
          <a href="/" className="back-link">← Back to Home</a>
        </div>
      </div>
    </div>
  );
}

export default Admin;
