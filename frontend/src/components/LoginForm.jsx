import React, { useState } from "react";
import "./LoginForm.css";

export default function LoginForm({ onLogin, onCreateAccount }) {
  const [role, setRole] = useState("individual");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin({ role, username, password });
  };

  return (
    <form className="login-form" onSubmit={handleSubmit}>
      <div className="logo">
        <span role="img" aria-label="GlyWatch Logo" style={{ fontSize: 48 }}>💧</span>
        <h1>GlyWatch</h1>
      </div>
      <div className="role-toggle">
        <button 
          type="button" 
          className={role === "individual" ? "active" : ""} 
          onClick={() => setRole("individual")}
        >
          Individual
        </button>
        <button 
          type="button" 
          className={role === "camp" ? "active" : ""} 
          onClick={() => setRole("camp")}
        >
          Camp
        </button>
      </div>
      <input 
        type="text" 
        placeholder="Username or Email" 
        value={username} 
        onChange={(e) => setUsername(e.target.value)} 
        required 
      />
      <input 
        type="password" 
        placeholder="Password" 
        value={password} 
        onChange={(e) => setPassword(e.target.value)} 
        required 
      />
      <button type="submit" className="login-btn">LOGIN</button>
      <button type="button" className="create-account-btn" onClick={onCreateAccount}>
        CREATE ACCOUNT
      </button>
    </form>
  );
} 