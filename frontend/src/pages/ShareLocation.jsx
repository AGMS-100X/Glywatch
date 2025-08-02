import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './ShareLocation.css';

export default function ShareLocation() {
  const navigate = useNavigate();
  const [isSharing, setIsSharing] = useState(false);
  const [currentLocation, setCurrentLocation] = useState({
    address: '569 W Berry St',
    city: 'Fort Wayne, IN',
    coordinates: { lat: 41.0793, lng: -85.1394 }
  });

  useEffect(() => {
    // Get current location on component mount
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setCurrentLocation({
            address: '569 W Berry St',
            city: 'Fort Wayne, IN',
            coordinates: {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            }
          });
        },
        () => {
          console.log('Unable to get location');
        }
      );
    }
  }, []);

  const handleBack = () => {
    navigate(-1);
  };

  const handleStartSharing = () => {
    setIsSharing(true);
    
    // Send location to backend
    fetch('/api/location/update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        latitude: currentLocation.coordinates.lat,
        longitude: currentLocation.coordinates.lng,
        address: currentLocation.address,
        city: currentLocation.city,
        timestamp: new Date().toISOString()
      })
    }).catch(error => {
      console.error('Error sharing location:', error);
    });
  };

  const handleStopSharing = () => {
    setIsSharing(false);
    
    // Stop location sharing
    fetch('/api/location/stop', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    }).catch(error => {
      console.error('Error stopping location sharing:', error);
    });
  };

  const handleCenterLocation = () => {
    // Center map on current location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setCurrentLocation({
            address: '569 W Berry St',
            city: 'Fort Wayne, IN',
            coordinates: {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            }
          });
        },
        () => {
          alert('Unable to get current location');
        }
      );
    }
  };

  return (
    <div className="share-location-page">
      {/* Header */}
      <div className="location-header">
        <button className="back-button" onClick={handleBack}>
          ←
        </button>
        <h1>Share Location</h1>
      </div>

      {/* Map Container */}
      <div className="map-container">
        <div className="map-placeholder">
          {/* Simulated map with streets */}
          <div className="map-streets">
            <div className="street street-1">W Washington Blvd</div>
            <div className="street street-2">W Uernington Blvd</div>
            <div className="street street-3">W Dewald St</div>
            <div className="river">Blue River</div>
          </div>
          
          {/* Location pin */}
          <div className="location-pin">📍</div>
          
          {/* Center location button */}
          <button className="center-location-btn" onClick={handleCenterLocation}>
            🎯
          </button>
        </div>
      </div>

      {/* Address Information */}
      <div className="address-info">
        <div className="address-text">
          <div className="street-address">{currentLocation.address}</div>
          <div className="city-state">{currentLocation.city}</div>
        </div>
      </div>

      {/* Action Button */}
      <div className="location-actions">
        {!isSharing ? (
          <button className="start-sharing-btn" onClick={handleStartSharing}>
            Start Sharing Location
          </button>
        ) : (
          <button className="stop-sharing-btn" onClick={handleStopSharing}>
            Stop Sharing
          </button>
        )}
      </div>
    </div>
  );
} 