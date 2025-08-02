import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import LoginForm from "../components/LoginForm";

export default function Login() {
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (data) => {
    setError("");
    
    // Mock authentication for frontend testing without backend
    if (data.role === "individual") {
      if (data.username === "patient" && data.password === "password") {
        // Store user info in localStorage
        localStorage.setItem("user", JSON.stringify({
          username: data.username,
          role: data.role,
          token: "mock-token-123"
        }));
        navigate("/dashboard");
        return;
      } else {
        setError("Invalid credentials for individual user");
        return;
      }
    } else if (data.role === "camp") {
      if (data.username === "caregiver" && data.password === "password") {
        // Store user info in localStorage
        localStorage.setItem("user", JSON.stringify({
          username: data.username,
          role: data.role,
          token: "mock-token-456"
        }));
        navigate("/caregiver");
        return;
      } else {
        setError("Invalid credentials for camp user");
        return;
      }
    }
    
    setError("Invalid role selected");
  };

  const handleCreateAccount = () => {
    // Redirect to registration page or show registration form
    alert("Redirect to registration page");
  };

  return (
    <div>
      <LoginForm onLogin={handleLogin} onCreateAccount={handleCreateAccount} />
      {error && (
        <div style={{ 
          color: "red", 
          marginTop: 16, 
          textAlign: "center",
          fontSize: "14px"
        }}>
          {error}
        </div>
      )}
    </div>
  );
} 