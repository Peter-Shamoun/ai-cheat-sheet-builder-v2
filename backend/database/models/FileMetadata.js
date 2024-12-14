// file-upload-app/database/models/FileMetadata.js

import mongoose from 'mongoose';

const fileMetadataSchema = new mongoose.Schema({
  filename: {
    type: String,
    required: true
  },
  mimetype: {
    type: String,
    required: true
  },
  size: {
    type: Number,
    required: true
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

const FileMetadata = mongoose.model('FileMetadata', fileMetadataSchema);

export default FileMetadata;
