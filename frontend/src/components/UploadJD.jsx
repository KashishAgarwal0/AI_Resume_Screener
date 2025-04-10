// UploadJD.jsx
import React, { useState } from 'react';

const UploadJD = ({ onUpload }) => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('jd', file);

    try {
      const res = await fetch('http://localhost:5000/upload-jd', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setMessage(data.message || data.error);
      onUpload(true);
    } catch (err) {
      console.error(err);
      setMessage('Error uploading JD');
    }
  };

  return (
    <div className="p-4 border rounded mb-4">
      <h2 className="text-xl font-semibold mb-2">Upload Job Description</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button className="bg-blue-500 text-white px-4 py-1 rounded ml-2" onClick={handleUpload}>Upload</button>
      {message && <p className="text-sm mt-2">{message}</p>}
    </div>
  );
};

export default UploadJD;