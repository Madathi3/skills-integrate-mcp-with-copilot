"""
Extracurricular Activity Management System
Flask application with database models for managing students, events, and activities.
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 
    f'sqlite:///{os.path.join(basedir, "activity_management.db")}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database
db = SQLAlchemy(app)

# Import models after db initialization
from src.models import (
    User, Student, Event, Attendance, Team, TeamMember,
    Workshop, WorkshopRegistration, Achievement, Progress
)

@app.route('/')
def index():
    """Home page route."""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'healthy', 'message': 'Server is running'}, 200

@app.shell_context_processor
def make_shell_context():
    """Make models available in Flask shell."""
    return {
        'db': db,
        'User': User,
        'Student': Student,
        'Event': Event,
        'Attendance': Attendance,
        'Team': Team,
        'TeamMember': TeamMember,
        'Workshop': Workshop,
        'WorkshopRegistration': WorkshopRegistration,
        'Achievement': Achievement,
        'Progress': Progress,
    }

def create_tables():
    """Create all database tables."""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    # Create tables on first run
    create_tables()
    app.run(debug=True, host='0.0.0.0', port=5000)
