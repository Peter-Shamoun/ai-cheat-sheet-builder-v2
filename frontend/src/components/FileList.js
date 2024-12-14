// file-upload-app/frontend/src/components/FileList.js

import React, { useEffect, useState } from 'react';

const FileList = () => {
  const [files, setFiles] = useState([]);

  const fetchFiles = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/files');
      if (response.ok) {
        const data = await response.json();
        setFiles(data);
      } else {
        console.error('Failed to fetch files');
      }
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  };

  useEffect(() => {
    fetchFiles();
    // Refresh the list every 5 seconds
    const interval = setInterval(fetchFiles, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleDelete = async (filename) => {
    try {
      const response = await fetch(`http://localhost:5000/api/upload/${encodeURIComponent(filename)}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        await fetchFiles(); // Refresh the list after successful deletion
      } else {
        const error = await response.json();
        alert(error.message || 'Failed to delete file');
      }
    } catch (error) {
      console.error('Error deleting file:', error);
      alert('Error deleting file');
    }
  };

  return (
    <div className="uploaded-files-container">
      <h2>Uploaded Files</h2>
      <ul className="uploaded-files-list">
        {files.map((file) => (
          <li key={file._id} className="uploaded-file-item">
            <span>{file.filename}</span>
            <button
              onClick={() => handleDelete(file.filename)}
              className="delete-button"
              aria-label="Delete file"
            >
              ×
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FileList;
