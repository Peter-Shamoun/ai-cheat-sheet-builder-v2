import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import FileMetadata from '../database/models/FileMetadata.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const uploadDir = path.join(__dirname, '../uploads');

const getFiles = async (req, res) => {
  try {
    // Get files from both database and filesystem
    const files = await FileMetadata.find({}).sort({ createdAt: -1 });
    
    // Log for debugging
    console.log('Files found in database:', files);
    
    // Verify files exist in filesystem
    const existingFiles = files.filter(file => {
      const filePath = path.join(uploadDir, file.filename);
      const exists = fs.existsSync(filePath);
      if (!exists) {
        console.log(`File ${file.filename} not found in filesystem`);
      }
      return exists;
    });

    res.status(200).json(existingFiles);
  } catch (error) {
    console.error('Error fetching files:', error);
    res.status(500).json({ message: 'Error fetching files', error: error.message });
  }
};

const uploadFiles = async (req, res) => {
  if (!req.files || req.files.length === 0) {
    return res.status(400).json({ message: 'No files uploaded' });
  }

  try {
    const fileMetadata = await Promise.all(
      req.files.map(async (file) => {
        const metadata = new FileMetadata({
          filename: file.filename,
          mimetype: file.mimetype,
          size: file.size,
          createdAt: new Date()
        });
        await metadata.save();
        console.log('Saved file metadata:', metadata); // Debug log
        return metadata;
      })
    );

    console.log('Upload successful, files:', fileMetadata); // Debug log
    res.status(200).json({ 
      message: 'Files uploaded successfully',
      files: fileMetadata 
    });
  } catch (error) {
    console.error('Error uploading files:', error);
    res.status(500).json({ message: 'Error uploading files', error: error.message });
  }
};

const cleanupUploads = async (req, res) => {
  try {
    // Delete all files in uploads directory
    const files = fs.readdirSync(uploadDir);
    for (const file of files) {
      fs.unlinkSync(path.join(uploadDir, file));
    }

    // Clear database records
    await FileMetadata.deleteMany({});

    res.status(200).json({ message: 'Upload directory cleaned successfully' });
  } catch (error) {
    console.error('Error cleaning upload directory:', error);
    res.status(500).json({ message: 'Error cleaning upload directory', error: error.message });
  }
};

const deleteFile = async (req, res) => {
  const { filename } = req.params;
  
  try {
    // Prevent directory traversal
    const safePath = path.join(uploadDir, path.basename(filename));
    
    // Check if file exists
    if (!fs.existsSync(safePath)) {
      return res.status(404).json({ message: 'File not found' });
    }

    // Delete file from filesystem
    fs.unlinkSync(safePath);
    
    // Delete metadata from database
    await FileMetadata.deleteOne({ filename: filename });
    
    res.status(200).json({ message: 'File deleted successfully' });
  } catch (error) {
    console.error('Error deleting file:', error);
    res.status(500).json({ message: 'Error deleting file', error: error.message });
  }
};

export { uploadFiles, getFiles, cleanupUploads, deleteFile };
