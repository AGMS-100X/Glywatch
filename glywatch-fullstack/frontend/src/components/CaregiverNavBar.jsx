import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import './NavBar.css';

export default function CaregiverNavBar() {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/');
  };

  return (
    <nav className="navbar caregiver-navbar">
      <div className="navbar-brand">
        <Link to="/caregiver">GLYWATCH CAMP</Link>
      </div>
      
      <div className="navbar-nav">
        <Link 
          to="/caregiver/cards" 
          className={`nav-link ${location.pathname === '/caregiver/cards' ? 'active' : ''}`}
        >
          Cards
        </Link>
        <Link 
          to="/caregiver" 
          className={`nav-link ${location.pathname === '/caregiver' ? 'active' : ''}`}
        >
          Grid
        </Link>
        <Link 
          to="/caregiver/timeline" 
          className={`nav-link ${location.pathname === '/caregiver/timeline' ? 'active' : ''}`}
        >
          Timeline
        </Link>
        <Link 
          to="/caregiver/map" 
          className={`nav-link ${location.pathname === '/caregiver/map' ? 'active' : ''}`}
        >
          Map
        </Link>
        <Link to="/alerts" className="nav-link">Alerts</Link>
        <Link to="/chat" className="nav-link">Chat</Link>
        <Link to="/admin" className="nav-link">Admin</Link>
      </div>
      
      <div className="navbar-menu">
        <button className="nav-icon-button logout-btn" onClick={handleLogout} title="Logout">
          🚪
        </button>
        <div className="navbar-menu-icon">
          ☰
        </div>
      </div>
    </nav>
  );
} 