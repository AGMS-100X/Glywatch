import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './GroupManagement.css';

export default function GroupManagement() {
  const navigate = useNavigate();
  const [contacts, setContacts] = useState([
    {
      id: 1,
      name: 'Lisa Mom',
      role: 'Primary caregiver',
      accessLevel: 'Full',
      accessColor: '#3b82f6'
    },
    {
      id: 2,
      name: 'John Dad',
      role: 'Secondary caregiver',
      accessLevel: 'Full',
      accessColor: '#3b82f6'
    },
    {
      id: 3,
      name: 'Emma Sister, 17',
      role: 'Family member',
      accessLevel: 'High',
      accessColor: '#10b981'
    },
    {
      id: 4,
      name: 'James Friend',
      role: 'Emergency contact',
      accessLevel: 'Low',
      accessColor: '#f59e0b'
    },
    {
      id: 5,
      name: 'Sarah Caregiver',
      role: 'Professional caregiver',
      accessLevel: 'Full',
      accessColor: '#3b82f6'
    }
  ]);

  const handleBack = () => {
    navigate(-1);
  };

  const handleAddContact = () => {
    // Open add contact modal or navigate to add contact page
    alert('Add new contact functionality');
  };

  const handleEditContact = (contactId) => {
    // Edit contact functionality
    alert(`Edit contact ${contactId}`);
  };

  const handleRemoveContact = (contactId) => {
    if (window.confirm('Are you sure you want to remove this contact?')) {
      setContacts(contacts.filter(contact => contact.id !== contactId));
    }
  };

  return (
    <div className="group-management-page">
      {/* Header */}
      <div className="group-header">
        <button className="back-button" onClick={handleBack}>
          ←
        </button>
        <h1>Group</h1>
      </div>

      {/* Contacts List */}
      <div className="contacts-list">
        {contacts.map((contact) => (
          <div key={contact.id} className="contact-item">
            <div className="contact-info">
              <div className="contact-name">{contact.name}</div>
              <div className="contact-role">{contact.role}</div>
            </div>
            <div className="contact-actions">
              <span 
                className="access-level"
                style={{ backgroundColor: contact.accessColor }}
              >
                {contact.accessLevel}
              </span>
              <div className="contact-buttons">
                <button 
                  className="edit-btn"
                  onClick={() => handleEditContact(contact.id)}
                >
                  ✏️
                </button>
                <button 
                  className="remove-btn"
                  onClick={() => handleRemoveContact(contact.id)}
                >
                  🗑️
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Add Contact Button */}
      <div className="add-contact-section">
        <button className="add-contact-btn" onClick={handleAddContact}>
          <span className="add-icon">+</span>
          <span className="add-text">Add</span>
        </button>
      </div>
    </div>
  );
} 