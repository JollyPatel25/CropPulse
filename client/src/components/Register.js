import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import "../pages/Login.css";

function Register({ onRegister }) {
  const [form, setForm] = useState({
    email: '', password: '', confirm_password: '', name: '', birth_date: '',
    street: '', city: '', state: '', pincode: ''
  });
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleRegister = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:5000/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });

    const data = await res.json();
    if (res.ok) {
      alert("Registration successful");
      localStorage.setItem("token", data.token);
      onRegister({ username: form.email, is_admin: false });
      navigate("/user");
    } else {
      alert(data.message || "Registration failed");
    }
  };

  return (
    <form onSubmit={handleRegister} className="auth-container">
      <h2>Register</h2>

      <label htmlFor="email">Email</label>
      <input name="email" type="email" onChange={handleChange} required />

      <label htmlFor="password">Password</label>
      <input name="password" type="password" onChange={handleChange} required />

      <label htmlFor="confirm_password">Confirm Password</label>
      <input name="confirm_password" type="password" onChange={handleChange} required />

      <label htmlFor="name">Full Name</label>
      <input name="name" onChange={handleChange} required />

      <label htmlFor="birth_date">Birth Date</label>
      <input name="birth_date" type="date" onChange={handleChange} required />

      <label htmlFor="street">Street</label>
      <input name="street" onChange={handleChange} required />

      <label htmlFor="city">City</label>
      <input name="city" onChange={handleChange} required />

      <label htmlFor="state">State</label>
      <input name="state" onChange={handleChange} required />

      <label htmlFor="pincode">Pincode</label>
      <input name="pincode" onChange={handleChange} required />

      <button type="submit">Register</button>
      <p>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </form>
  );
}

export default Register;
