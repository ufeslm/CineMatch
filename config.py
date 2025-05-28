import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    
    # Database Configuration
    # For production, use Supabase PostgreSQL URL
    # For development, fallback to SQLite
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        # Fix for SQLAlchemy 1.4+ compatibility
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # TMDB API Configuration
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY') or 'b58a5f26fe980d389eb8f043060f8470'
    TMDB_BASE_URL = 'https://api.themoviedb.org/3'
    
    # Email Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'recommendationsmovies630@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'wsfm injo hvfd bddf'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'recommendationsmovies630@gmail.com' 