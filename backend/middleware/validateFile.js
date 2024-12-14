// file-upload-app/backend/middleware/validateFile.js

const validateFile = (req, res, next) => {
    if (!req.files || req.files.length === 0) {
      return res.status(400).json({ message: 'No files were uploaded' });
    }
  
    const allowedTypes = ['image/png', 'image/jpeg', 'application/pdf', 'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'];
    const maxFiles = 50;
  
    if (req.files.length > maxFiles) {
      return res.status(400).json({ message: `You can only upload up to ${maxFiles} files` });
    }
  
    for (const file of req.files) {
      if (!allowedTypes.includes(file.mimetype)) {
        return res.status(400).json({ message: `File type ${file.mimetype} is not allowed` });
      }
    }
  
    next();
  };
  
  export default validateFile;
  