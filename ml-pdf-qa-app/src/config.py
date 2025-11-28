# Configuration settings for the PDF QA application

class Config:
    PDF_UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'pdf'}
    MODEL_PATH = 'models/qa_model.bin'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for uploaded files
    SECRET_KEY = 'your_secret_key_here'  # Change this to a random secret key for production
    DEBUG = True  # Set to False in production