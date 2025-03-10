import os

class Config:
    SECRET_KEY = 'King'
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1 MB max upload
    UPLOAD_EXTENSIONS = [".jpg", ".png"]
    UPLOAD_PATH = 'uploads/'
    DATABASE = "./SQL/student.db"
