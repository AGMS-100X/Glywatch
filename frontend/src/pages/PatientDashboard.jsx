import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import IndividualNavBar from '../components/IndividualNavBar';
import './Dashboard.css';

export default function PatientDashboard() {
  const navigate = useNavigate();
  const [glucoseReading, setGlucoseReading] = useState(104);
  const [glucoseStatus, setGlucoseStatus] = useState('Normal');
  const [lastUpdate, setLastUpdate] = useState('2 minutes ago');

  useEffect(() => {
    // Simulate real-time glucose updates
    const interval = setInterval(() => {
      // Simulate glucose changes
      const newReading = Math.floor(Math.random() * 50) + 80;
      setGlucoseReading(newReading);
      
      // Update status based on reading
      if (newReading < 70) setGlucoseStatus('Low');
      else if (newReading > 180) setGlucoseStatus('High');
      else setGlucoseStatus('Normal');
      
      setLastUpdate('Just now');
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const handleSOS = () => {
    navigate('/sos');
  };

  const handleGroup = () => {
    navigate('/group');
  };

  const handleShareLocation = () => {
    navigate('/share-location');
  };

  const handleChat = () => {
    navigate('/chat');
  };

  return (
    <div className="dashboard-page individual-dashboard">
      <IndividualNavBar />
      
      <div className="dashboard-content">
        {/* Patient Monitoring Section */}
        <div className="monitoring-section">
          <h2>Patient Monitoring</h2>
          
          <div className="glucose-display">
            <div className="glucose-reading">
              <span className="glucose-value">{glucoseReading}</span>
              <span className="glucose-unit">mg/dL</span>
            </div>
            
            <div className="glucose-status">
              <span className={`status-badge ${glucoseStatus.toLowerCase()}`}>
                {glucoseStatus}
              </span>
            </div>
          </div>
          
          <div className="glucose-trend">
            <div className="trend-graph">
              {/* Simple trend visualization */}
              <div className="trend-line">
                <div className="trend-point" style={{height: '20%'}}></div>
                <div className="trend-point" style={{height: '40%'}}></div>
                <div className="trend-point" style={{height: '30%'}}></div>
                <div className="trend-point" style={{height: '60%'}}></div>
                <div className="trend-point" style={{height: '50%'}}></div>
                <div className="trend-point" style={{height: '70%'}}></div>
                <div className="trend-point active" style={{height: '80%'}}></div>
              </div>
            </div>
            <span className="last-update">Last update: {lastUpdate}</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="action-buttons">
          <button className="action-btn sos-btn" onClick={handleSOS}>
            <span className="btn-icon">🚨</span>
            <span className="btn-text">SOS</span>
          </button>
          
          <button className="action-btn" onClick={handleChat}>
            <span className="btn-icon">💬</span>
            <span className="btn-text">Messages</span>
          </button>
          
          <button className="action-btn" onClick={handleShareLocation}>
            <span className="btn-icon">📍</span>
            <span className="btn-text">Share Location</span>
          </button>
          
          <button className="action-btn" onClick={handleGroup}>
            <span className="btn-icon">👥</span>
            <span className="btn-text">Group</span>
          </button>
        </div>

        {/* Dashboards Section */}
        <div className="dashboards-section">
          <h3>Dashboards</h3>
          
          <div className="dashboard-cards">
            <div className="dashboard-card glucose-card">
              <h4>Glucose</h4>
              <div className="card-content">
                <div className="mini-chart">
                  <div className="chart-bar" style={{height: '60%'}}></div>
                  <div className="chart-bar" style={{height: '80%'}}></div>
                  <div className="chart-bar" style={{height: '40%'}}></div>
                  <div className="chart-bar" style={{height: '90%'}}></div>
                  <div className="chart-bar" style={{height: '70%'}}></div>
                  <div className="chart-bar" style={{height: '50%'}}></div>
                  <div className="chart-bar" style={{height: '85%'}}></div>
                </div>
                <div className="chart-labels">
                  <span>MON</span>
                  <span>TUE</span>
                  <span>WED</span>
                  <span>THU</span>
                  <span>FRI</span>
                  <span>SAT</span>
                  <span>SUN</span>
                </div>
              </div>
            </div>
            
            <div className="dashboard-card messages-card">
              <h4>Messages</h4>
              <div className="card-content">
                <div className="message-list">
                  <div className="message-line"></div>
                  <div className="message-line"></div>
                  <div className="message-line"></div>
                </div>
              </div>
            </div>
            
            <div className="dashboard-card location-card">
              <h4>Location</h4>
              <div className="card-content">
                <div className="map-placeholder">
                  <span className="map-pin">📍</span>
                </div>
              </div>
            </div>
            
            <div className="dashboard-card alerts-card">
              <h4>Alerts</h4>
              <div className="card-content">
                <div className="alert-indicators">
                  <span className="alert-icon">⚠️</span>
                  <div className="alert-dots">
                    <span className="dot"></span>
                    <span className="dot"></span>
                    <span className="dot active"></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 