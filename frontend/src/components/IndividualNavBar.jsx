import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './NavBar.css';

export default function IndividualNavBar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/');
  };

  return (
    <nav className="navbar individual-navbar">
      <div className="navbar-left">
        <button className="back-button" onClick={() => navigate(-1)}>
          ←
        </button>
        <span className="navbar-title">DIABETES REMOTE MONITORING</span>
      </div>
      
      <div className="navbar-right">
        <Link to="/sos" className="nav-icon-button" title="SOS">
          🚨
        </Link>
        <Link to="/group" className="nav-icon-button" title="Group">
          👥
        </Link>
        <Link to="/share-location" className="nav-icon-button" title="Share Location">
          📍
        </Link>
        <Link to="/chat" className="nav-icon-button" title="Chat">
          💬
        </Link>
        <Link to="/settings" className="nav-icon-button" title="Settings">
          ⚙️
        </Link>
        <button className="nav-icon-button logout-btn" onClick={handleLogout} title="Logout">
          🚪
        </button>
      </div>
    </nav>
  );
} 