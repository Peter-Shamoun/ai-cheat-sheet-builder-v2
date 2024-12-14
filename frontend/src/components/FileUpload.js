import React, { useState, useRef, useEffect } from 'react';

const FileUpload = () => {
  const [files, setFiles] = useState([]);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const uploadedFiles = Array.from(event.target.files);
    setFiles((prevFiles) => [...prevFiles, ...uploadedFiles]);
  };

  const resetFileInput = () => {
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    setFiles([]);
  };

  const fetchUploadedFiles = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/files');
      if (response.ok) {
        const data = await response.json();
        setUploadedFiles(data);
      }
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  };

  useEffect(() => {
    fetchUploadedFiles();
  }, []);

  const handleDelete = async (filename) => {
    try {
      const response = await fetch(`http://localhost:5000/api/upload/${encodeURIComponent(filename)}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setUploadedFiles(prevFiles => prevFiles.filter(file => file.filename !== filename));
      } else {
        const error = await response.json();
        alert(error.message || 'Failed to delete file');
      }
    } catch (error) {
      console.error('Error deleting file:', error);
      alert('Error deleting file');
    }
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));

    try {
      console.log('Attempting to upload files...');
      const response = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
        },
        body: formData,
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('Upload successful:', result);
        alert('Files uploaded successfully');
        resetFileInput();
        fetchUploadedFiles(); // Refresh the file list
      } else {
        const errorData = await response.json();
        console.error('Upload failed:', errorData);
        alert(errorData.message || 'Failed to upload files');
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Error uploading files: ' + error.message);
    }
  };

  return (
    <div className="upload-container">
      <div className="file-input-container">
        <label className="file-input-label">
          Choose Files
          <input
            ref={fileInputRef}
            type="file"
            multiple
            onChange={handleFileChange}
            className="file-input"
          />
        </label>
      </div>
      {files.length > 0 && (
        <>
          <ul className="file-list">
            {files.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
          <button onClick={handleSubmit} className="upload-button">
            Upload {files.length} {files.length === 1 ? 'File' : 'Files'}
          </button>
        </>
      )}
      
      {uploadedFiles.length > 0 && (
        <div className="uploaded-files-container">
          <h3>Uploaded Files</h3>
          <ul className="uploaded-files-list">
            {uploadedFiles.map((file) => (
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
      )}
    </div>
  );
};

export default FileUpload;
