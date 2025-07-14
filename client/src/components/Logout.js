import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Logout({ onLogout }) {
  const navigate = useNavigate();

  useEffect(() => {
    onLogout();  // Clear user and token
    navigate('/');
  }, [navigate, onLogout]);

  return <p>Logging out...</p>;
}

export default Logout;
