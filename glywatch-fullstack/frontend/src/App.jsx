import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import PatientDashboard from "./pages/PatientDashboard";
import CaregiverDashboard from "./pages/CaregiverDashboard";
import SOSRequests from "./pages/SOSRequests";
import GroupManagement from "./pages/GroupManagement";
import ShareLocation from "./pages/ShareLocation";
import AlertsCenter from "./pages/AlertsCenter";
import ChatPage from "./pages/ChatPage";
import Reports from "./pages/Reports";
import Settings from "./pages/Settings";
import AdminPanel from "./pages/AdminPanel";
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<PatientDashboard />} />
        <Route path="/caregiver" element={<CaregiverDashboard />} />
        
        {/* Individual User Routes */}
        <Route path="/sos" element={<SOSRequests />} />
        <Route path="/group" element={<GroupManagement />} />
        <Route path="/share-location" element={<ShareLocation />} />
        
        {/* Nested routes for caregiver dashboard views */}
        <Route path="/caregiver/cards" element={<CaregiverDashboard />} />
        <Route path="/caregiver/timeline" element={<CaregiverDashboard />} />
        <Route path="/caregiver/map" element={<CaregiverDashboard />} />
        
        <Route path="/alerts" element={<AlertsCenter />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/admin" element={<AdminPanel />} />
      </Routes>
    </Router>
  );
}

export default App; 