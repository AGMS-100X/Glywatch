import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './SOSRequests.css';

export default function SOSRequests() {
  const navigate = useNavigate();
  const [sosHistory, setSosHistory] = useState([
    {
      id: 1,
      timestamp: 'Just now',
      type: 'Manual',
      description: 'Manual SOS alert triggered'
    },
    {
      id: 2,
      timestamp: 'Today, 11:15 AM',
      type: 'Automated',
      description: 'Automated alert due to glucose levels'
    },
    {
      id: 3,
      timestamp: 'Yesterday, 9:42 PM',
      type: 'Automated',
      description: 'Automated alert due to rapid glucose drop'
    },
    {
      id: 4,
      timestamp: 'April 18, 2024, 2:28 PM',
      type: 'Manual',
      description: 'Manual SOS alert triggered'
    }
  ]);

  const handleBack = () => {
    navigate(-1);
  };

  const handleNewSOS = () => {
    // Trigger new SOS alert
    const newSOS = {
      id: Date.now(),
      timestamp: 'Just now',
      type: 'Manual',
      description: 'Manual SOS alert triggered'
    };
    setSosHistory([newSOS, ...sosHistory]);
    
    // Send SOS to backend
    fetch('/api/sos/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        type: 'manual',
        timestamp: new Date().toISOString(),
        description: 'Manual SOS alert triggered'
      })
    }).catch(error => {
      console.error('Error sending SOS:', error);
    });
  };

  return (
    <div className="sos-requests-page">
      {/* Header */}
      <div className="sos-header">
        <button className="back-button" onClick={handleBack}>
          ←
        </button>
        <h1>SOS Requests</h1>
      </div>

      {/* Description */}
      <div className="sos-description">
        <p>History of SOS alerts sent from this device</p>
      </div>

      {/* SOS History List */}
      <div className="sos-history">
        {sosHistory.map((sos) => (
          <div key={sos.id} className="sos-item">
            <div className="sos-icon">
              <span className="alert-icon">⚠️</span>
            </div>
            <div className="sos-content">
              <div className="sos-timestamp">{sos.timestamp}</div>
              <div className="sos-type">{sos.type}</div>
            </div>
          </div>
        ))}
      </div>

      {/* New SOS Button */}
      <div className="sos-actions">
        <button className="new-sos-btn" onClick={handleNewSOS}>
          🚨 Send New SOS Alert
        </button>
      </div>
    </div>
  );
} 