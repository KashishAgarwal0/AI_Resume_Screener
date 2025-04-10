// UploadResume.jsx
import React, { useState } from 'react';

const UploadResume = ({ onExtract }) => {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append('resume', file);

    try {
      const res = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      onExtract(data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="p-4 border rounded mb-4">
      <h2 className="text-xl font-semibold mb-2">Upload Resume</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button className="bg-green-600 text-white px-4 py-1 rounded ml-2" onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default UploadResume;