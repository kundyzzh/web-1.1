from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_handler import main_bp  # Ensure this is your Flask blueprint
from fastapi_handler import app as fastapi_app  # Your FastAPI app should be defined in fastapi_handler.py
import threading
import uvicorn
from UserModel import db
# Initialize the Flask app
flask_app = Flask(__name__)
flask_app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Configure the database
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'  # SQLite database
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications

# Initialize the SQLAlchemy database instance
db.init_app(flask_app)

# Register the blueprint
flask_app.register_blueprint(main_bp)

def create_database():
    """Create database tables within the Flask app context."""
    with flask_app.app_context():
        db.create_all()  # Create database tables defined in your models

def run_fastapi():
    """Run the FastAPI application in a separate thread."""
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8001)

def run_flask_app():
    """Run the Flask application."""
    flask_app.run(debug=True, port=5000)  # Start Flask app in debug mode on port 5000

if __name__ == '__main__':
    # Create the database tables
    create_database()

    # Start FastAPI in a separate thread
    threading.Thread(target=run_fastapi, daemon=True).start()

    # Run the Flask application
    run_flask_app()
