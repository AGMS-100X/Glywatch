import React, { useState, useEffect } from 'react';
import CaregiverNavBar from '../components/CaregiverNavBar';
import './Dashboard.css';

export default function CaregiverDashboard() {
  const [patients, setPatients] = useState([
    {
      id: 1,
      name: 'Emma Johnson',
      glucose: 52,
      status: 'critical',
      description: 'Rapid drop detected',
      lastUpdate: '2m ago',
      hasAlert: true
    },
    {
      id: 2,
      name: 'Jacob Smith',
      glucose: 70,
      status: 'normal',
      description: 'Steady pot-meal',
      lastUpdate: '5m ago',
      hasAlert: false
    },
    {
      id: 3,
      name: 'Olivia Brown',
      glucose: 106,
      status: 'normal',
      description: 'Stable overnight',
      lastUpdate: '20m ago',
      hasAlert: false
    },
    {
      id: 4,
      name: 'Ethan Williams',
      glucose: 132,
      status: 'normal',
      description: 'No recent issues',
      lastUpdate: '45m ago',
      hasAlert: false
    }
  ]);

  const [filters, setFilters] = useState({
    alertLevel: 'All alert levels',
    location: 'All locations',
    sortBy: 'Sort by'
  });

  const [statusCounts, setStatusCounts] = useState({
    critical: 2,
    high: 4,
    normal: 22
  });

  useEffect(() => {
    // Simulate real-time updates
    const interval = setInterval(() => {
      setPatients(prevPatients => 
        prevPatients.map(patient => ({
          ...patient,
          glucose: Math.floor(Math.random() * 100) + 50,
          lastUpdate: 'Just now'
        }))
      );
    }, 60000); // Update every minute

    return () => clearInterval(interval);
  }, []);

  const handleAlert = (patientId) => {
    alert(`Alert sent for ${patients.find(p => p.id === patientId)?.name}`);
  };

  const handleMessage = (patientId) => {
    alert(`Opening chat with ${patients.find(p => p.id === patientId)?.name}`);
  };

  const handleView = (patientId) => {
    alert(`Viewing details for ${patients.find(p => p.id === patientId)?.name}`);
  };

  return (
    <div className="dashboard-page caregiver-dashboard">
      <CaregiverNavBar />
      
      <div className="dashboard-content">
        {/* Header */}
        <div className="dashboard-header">
          <h1>Sunset Lake Camp</h1>
          <p className="date-range">July 8-14</p>
        </div>

        {/* Filters and Status Summary */}
        <div className="filters-summary">
          <div className="filter-group">
            <select 
              className="filter-dropdown"
              value={filters.alertLevel}
              onChange={(e) => setFilters({...filters, alertLevel: e.target.value})}
            >
              <option>All alert levels</option>
              <option>Critical</option>
              <option>High</option>
              <option>Normal</option>
            </select>
            
            <select 
              className="filter-dropdown"
              value={filters.location}
              onChange={(e) => setFilters({...filters, location: e.target.value})}
            >
              <option>All locations</option>
              <option>Sunset Lake Camp</option>
              <option>Pine Ridge Camp</option>
            </select>
            
            <select 
              className="filter-dropdown"
              value={filters.sortBy}
              onChange={(e) => setFilters({...filters, sortBy: e.target.value})}
            >
              <option>Sort by</option>
              <option>Alert Level</option>
              <option>Last Update</option>
              <option>Name</option>
            </select>
          </div>
          
          <div className="status-summary">
            <span className="status-pill critical">
              ⚠️ {statusCounts.critical} critical
            </span>
            <span className="status-pill high">
              🔶 {statusCounts.high} high
            </span>
            <span className="status-pill normal">
              ✅ {statusCounts.normal} normal
            </span>
          </div>
        </div>

        {/* Patient Grid */}
        <div className="patient-grid">
          {patients.map(patient => (
            <div key={patient.id} className={`patient-card ${patient.status}-card`}>
              <div className="card-header">
                <img 
                  src={`https://via.placeholder.com/50/2563eb/ffffff?text=${patient.name.charAt(0)}`}
                  alt={patient.name}
                  className="profile-pic"
                />
                <h3>{patient.name}</h3>
              </div>
              
              <div className="card-body">
                <div className="glucose-reading">
                  <span className="glucose-value">{patient.glucose}</span>
                  {patient.status === 'critical' && (
                    <span className="status-indicator critical">⚠️ Critical</span>
                  )}
                  {patient.status === 'normal' && (
                    <span className="trend-icon">↗</span>
                  )}
                </div>
                
                <p className="description">{patient.description}</p>
                
                <div className="card-actions">
                  {patient.hasAlert && (
                    <button 
                      className="btn-alert"
                      onClick={() => handleAlert(patient.id)}
                    >
                      Alert
                    </button>
                  )}
                  <button 
                    className="btn-message"
                    onClick={() => handleMessage(patient.id)}
                  >
                    Message
                  </button>
                  {!patient.hasAlert && (
                    <button 
                      className="btn-view"
                      onClick={() => handleView(patient.id)}
                    >
                      View
                    </button>
                  )}
                </div>
              </div>
              
              <div className="card-footer">
                <span>Last update: {patient.lastUpdate}</span>
                <span className="dropdown-arrow">▼</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
} 