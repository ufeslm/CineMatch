import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # TMDB API Configuration
    TMDB_API_KEY = 'b58a5f26fe980d389eb8f043060f8470'
    TMDB_BASE_URL = 'https://api.themoviedb.org/3'
    
    # Email Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'recommendationsmovies630@gmail.com'
    MAIL_PASSWORD = 'wsfm injo hvfd bddf'
    MAIL_DEFAULT_SENDER = 'recommendationsmovies630@gmail.com' 