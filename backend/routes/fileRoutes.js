import express from 'express';
import { uploadFiles, getFiles, cleanupUploads, deleteFile } from '../controllers/fileController.js';
import validateFile from '../middleware/validateFile.js';
import upload from '../middleware/upload.js';

const router = express.Router();

// Files routes
router.get('/files', getFiles);
router.post('/upload', upload.array('files'), validateFile, uploadFiles);
router.delete('/files/:filename', deleteFile);
router.post('/cleanup', cleanupUploads);

export default router;
