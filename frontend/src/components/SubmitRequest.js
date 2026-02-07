import React, { useState } from 'react';
import axios from 'axios';
import './SubmitRequest.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function SubmitRequest() {
  const [formData, setFormData] = useState({
    homeowner_name: '',
    email: '',
    address: '',
    change_type: '',
    description: '',
    urgency: 'normal'
  });
  const [submitted, setSubmitted] = useState(false);
  const [requestId, setRequestId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const changeTypes = [
    'Exterior Painting',
    'Landscaping',
    'Fence Installation',
    'Solar Panels',
    'Roof Replacement',
    'Deck/Patio Addition',
    'Window Replacement',
    'Other'
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_URL}/api/submit-request`, formData);
      setRequestId(response.data.request_id);
      setSubmitted(true);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit request. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      homeowner_name: '',
      email: '',
      address: '',
      change_type: '',
      description: '',
      urgency: 'normal'
    });
    setSubmitted(false);
    setRequestId('');
  };

  if (submitted) {
    return (
      <div className="submit-request-container">
        <div className="success-card">
          <div className="success-icon">✓</div>
          <h2>Request Submitted Successfully!</h2>
          <p className="request-id">Request ID: <strong>{requestId}</strong></p>
          <p className="success-message">
            Your request has been submitted to the HOA board. 
            You will receive a confirmation email at <strong>{formData.email}</strong>.
            The board typically reviews requests within 5-10 business days.
          </p>
          <button className="new-request-btn" onClick={resetForm}>
            Submit Another Request
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="submit-request-container">
      <div className="request-card">
        <h2>Submit Home Modification Request</h2>
        <p className="subtitle">Request permission for changes to your property</p>

        <form onSubmit={handleSubmit} className="request-form">
          <div className="form-group">
            <label htmlFor="homeowner_name">Full Name *</label>
            <input
              type="text"
              id="homeowner_name"
              name="homeowner_name"
              value={formData.homeowner_name}
              onChange={handleChange}
              required
              placeholder="John Doe"
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email Address *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="john.doe@example.com"
            />
          </div>

          <div className="form-group">
            <label htmlFor="address">Property Address *</label>
            <input
              type="text"
              id="address"
              name="address"
              value={formData.address}
              onChange={handleChange}
              required
              placeholder="123 Main Street"
            />
          </div>

          <div className="form-group">
            <label htmlFor="change_type">Type of Change *</label>
            <select
              id="change_type"
              name="change_type"
              value={formData.change_type}
              onChange={handleChange}
              required
            >
              <option value="">Select a type</option>
              {changeTypes.map((type, index) => (
                <option key={index} value={type}>{type}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="description">Description *</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              rows="5"
              placeholder="Please provide detailed information about the proposed changes, including materials, colors, dimensions, etc."
            />
          </div>

          <div className="form-group">
            <label htmlFor="urgency">Urgency</label>
            <select
              id="urgency"
              name="urgency"
              value={formData.urgency}
              onChange={handleChange}
            >
              <option value="normal">Normal</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Submitting...' : 'Submit Request'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default SubmitRequest;
