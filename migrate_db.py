#!/usr/bin/env python3
"""
Database migration script for Supabase deployment
Run this once after deployment to create tables
"""

import os
from app import create_app, db

def init_db():
    """Initialize database tables"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Print table info
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📋 Created tables: {', '.join(tables)}")

if __name__ == "__main__":
    init_db() 