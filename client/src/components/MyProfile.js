import React, { useEffect, useState } from 'react';
import '../pages/MyProfile.css';
import defaultProfile from '../assets/default-profile.jpg';

function MyProfile({user, adminOnly}) {
  const [form, setForm] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);

  const token = localStorage.getItem("token");

  useEffect(() => {
    if (!token) {
      alert("Please login first.");
      return;
    }

    fetch('http://localhost:5000/auth/profile', {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => {
        setForm(data);
        if (data.profile_image) {
          setImagePreview(`http://localhost:5000/uploads/${data.profile_image}`);
        } else {
          setImagePreview(defaultProfile);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        alert("Failed to load profile.");
        setLoading(false);
      });
  }, [token]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name in form.address) {
      setForm(prev => ({ ...prev, address: { ...prev.address, [name]: value } }));
    } else {
      setForm(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImagePreview(URL.createObjectURL(file));
      setForm(prev => ({ ...prev, profile_image_file: file }));
    }
  };

    const handleImageDelete = async () => {
    const confirmed = window.confirm("Are you sure you want to delete your profile photo?");
    if (!confirmed) return;

    try {
        const imageName = form.profile_image;
        const res = await fetch(`http://localhost:5000/auth/delete-image?image=${encodeURIComponent(imageName)}`, {
        method: 'DELETE',
        headers: {
            Authorization: `Bearer ${token}`
        }
        });

        const data = await res.json();
        if (res.ok) {
        alert("🗑️ Profile photo deleted.");
        setForm(prev => ({ ...prev, profile_image: null }));
        setImagePreview(defaultProfile);
        } else {
        alert(data.message || "Failed to delete image.");
        }
    } catch (err) {
        console.error(err);
        alert("Error deleting profile photo.");
    }
    };


  const handleSubmit = async () => {
    const { name, birth_date, address } = form;
    if (!name?.trim() || !birth_date?.trim() ||
        !address?.street?.trim() || !address?.city?.trim() ||
        !address?.state?.trim() || !address?.pincode?.trim()) {
      alert("🚫 All fields are required. Please fill in all values.");
      return;
    }

    const formData = new FormData();
    formData.append("name", name);
    formData.append("birth_date", birth_date);
    formData.append("street", address.street);
    formData.append("city", address.city);
    formData.append("state", address.state);
    formData.append("pincode", address.pincode);
    if (form.profile_image_file) {
      formData.append("profile_image", form.profile_image_file);
    }

    try {
      const res = await fetch('http://localhost:5000/auth/profile', {
        method: 'PUT',
        headers: { Authorization: `Bearer ${token}` },
        body: formData
      });

      const updated = await res.json();
      alert("✅ Profile updated!");
      setForm(updated);
      setEditing(false);
      setImagePreview(`http://localhost:5000/uploads/${updated.profile_image}?t=${Date.now()}`);
    } catch (err) {
      alert("Failed to update profile.");
      console.error(err);
    }
  };

  if (loading || !form) return <div className="profile-container">Loading...</div>;

  return (
    <div className="profile-container">
      <h2>My Profile</h2>
      <div className="profile-card">
        <div className="image-section">
          <img
            src={imagePreview || defaultProfile}
            alt="Profile"
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = defaultProfile;
            }}
          />
          {editing && (
            <>
                <input type="file" accept="image/*" onChange={handleImageChange} />
                {form.profile_image && (
                <button
                    type="button"
                    className="delete-photo-button"
                    onClick={handleImageDelete}
                >
                   🗑️ Delete Photo
                </button>
                )}
            </>
            )}

        </div>
        <div className="profile-details">
          <p><strong>Email:</strong> {form.email}</p>
          <p>
            <label>Name:
              <input type="text" name="name" value={form.name} onChange={handleChange} disabled={!editing} />
            </label>
          </p>
          <p>
            <label>Birth Date:
              <input type="date" name="birth_date" value={form.birth_date} onChange={handleChange} disabled={!editing} />
            </label>
          </p>
          <h4>Address</h4>
            {!editing ? (
            <p>{[form.address.street, form.address.city, form.address.state, form.address.pincode].filter(Boolean).join(", ")}</p>
            ) : (
            <>
                <p><label>Street: <input name="street" value={form.address.street} onChange={handleChange} /></label></p>
                <p><label>City: <input name="city" value={form.address.city} onChange={handleChange} /></label></p>
                <p><label>State: <input name="state" value={form.address.state} onChange={handleChange} /></label></p>
                <p><label>Pincode: <input name="pincode" value={form.address.pincode} onChange={handleChange} /></label></p>
            </>
            )}

          {!editing ? (
            <button onClick={() => setEditing(true)}>Edit Profile</button>
          ) : (
            <div>
              <button onClick={handleSubmit}>Save Changes</button>
              <button className="cancel-button" onClick={() => setEditing(false)}>Cancel</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default MyProfile;