#!/usr/bin/env python3
"""
Deployment helper script for Movie Recommendation System
Run this script to test your app locally before deploying
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if all required packages are installed"""
    print("🔍 Checking requirements...")
    try:
        import flask
        import flask_sqlalchemy
        import flask_login
        import requests
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def check_env_vars():
    """Check if environment variables are set"""
    print("\n🔍 Checking environment variables...")
    
    required_vars = ['SECRET_KEY', 'TMDB_API_KEY']
    optional_vars = ['MAIL_USERNAME', 'MAIL_PASSWORD']
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.environ.get(var):
            missing_optional.append(var)
    
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        print("Create a .env file with these variables or set them in your deployment platform")
        return False
    else:
        print("✅ All required environment variables are set")
    
    if missing_optional:
        print(f"⚠️  Optional variables not set: {', '.join(missing_optional)}")
        print("Email notifications will not work without these")
    
    return True

def test_tmdb_api():
    """Test TMDB API connection"""
    print("\n🔍 Testing TMDB API connection...")
    
    api_key = os.environ.get('TMDB_API_KEY')
    if not api_key:
        print("❌ TMDB_API_KEY not set")
        return False
    
    try:
        import requests
        url = f"https://api.themoviedb.org/3/movie/550?api_key={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ TMDB API connection successful")
            return True
        else:
            print(f"❌ TMDB API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ TMDB API connection failed: {e}")
        return False

def run_local_test():
    """Run the app locally for testing"""
    print("\n🚀 Starting local test server...")
    print("Visit http://localhost:5000 to test your app")
    print("Press Ctrl+C to stop")
    
    try:
        from app import create_app
        app = create_app()
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    print("🎬 Movie Recommendation System - Deployment Helper")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment variables
    env_ok = check_env_vars()
    
    # Test API
    api_ok = test_tmdb_api()
    
    print("\n" + "=" * 50)
    
    if env_ok and api_ok:
        print("✅ All checks passed! Your app is ready for deployment")
        
        choice = input("\nWould you like to test locally? (y/n): ").lower().strip()
        if choice == 'y':
            run_local_test()
    else:
        print("❌ Some checks failed. Please fix the issues before deploying")
        print("\nNext steps:")
        print("1. Get a TMDB API key from https://www.themoviedb.org/settings/api")
        print("2. Set your environment variables")
        print("3. Run this script again")

if __name__ == "__main__":
    main() 