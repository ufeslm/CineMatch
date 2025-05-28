from app import create_app, db
from flask import jsonify

def handler(request):
    """Initialize database tables via HTTP request"""
    try:
        app = create_app()
        
        with app.app_context():
            # Create all tables
            db.create_all()
            
            # Get table info
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            return {
                "statusCode": 200,
                "body": {
                    "message": "Database tables created successfully!",
                    "tables": tables
                }
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": {
                "error": str(e),
                "message": "Failed to initialize database"
            }
        } 