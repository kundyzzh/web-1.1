# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_handler import main_bp
from fastapi import FastAPI
import threading

# Initialize the Flask app
flask_app = Flask(__name__)
flask_app.secret_key = 'your_secret_key'  # Set a secret key for sessions

# Configure the database
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'  # You can choose your database here
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications

# Initialize the database
db = SQLAlchemy(flask_app)

# Register the blueprint
flask_app.register_blueprint(main_bp)

# FastAPI integration
from fastapi_handler import app as fastapi_app

def run_fastapi():
    import uvicorn
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8001)

# Create a function to run the application
def run_app():
    with flask_app.app_context():
        db.create_all()  # Ensure your tables are created
    flask_app.run(debug=True, port=5000)  # Run the Flask app in debug mode

if __name__ == '__main__':
    # Start FastAPI in a separate thread
    threading.Thread(target=run_fastapi, daemon=True).start()
    run_app()  # Run the Flask app
