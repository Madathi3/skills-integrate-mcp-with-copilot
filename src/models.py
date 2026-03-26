"""
Database models for the Extracurricular Activity Management System.
Using Flask-SQLAlchemy ORM with support for complex relationships.
"""

from datetime import datetime
from sqlalchemy import Enum
import enum


class User(db.Model):
    """User model for authentication and authorization."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), default='user', nullable=False)  # user, admin, moderator
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    students = db.relationship('Student', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Student(db.Model):
    """Student model for managing student profiles and information."""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    major = db.Column(db.String(120))
    batch_year = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendances = db.relationship('Attendance', backref='student', lazy=True, cascade='all, delete-orphan')
    achievements = db.relationship('Achievement', backref='student', lazy=True, cascade='all, delete-orphan')
    team_members = db.relationship('TeamMember', backref='student', lazy=True, cascade='all, delete-orphan')
    workshop_registrations = db.relationship('WorkshopRegistration', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.student_id}>'


class Event(db.Model):
    """Event model for managing events and scheduling."""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    start_date = db.Column(db.DateTime, nullable=False, index=True)
    end_date = db.Column(db.DateTime)
    capacity = db.Column(db.Integer)
    organizer = db.Column(db.String(120))
    status = db.Column(db.String(50), default='scheduled')  # scheduled, ongoing, completed, cancelled
    banner_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendances = db.relationship('Attendance', backref='event', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Event {self.title}>'


class Attendance(db.Model):
    """Attendance model for tracking attendance records."""
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False, index=True)
    check_in_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    check_out_time = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='present')  # present, absent, excused
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite unique constraint
    __table_args__ = (db.UniqueConstraint('student_id', 'event_id', name='unique_student_event'),)
    
    def __repr__(self):
        return f'<Attendance Student:{self.student_id} Event:{self.event_id}>'


class Team(db.Model):
    """Team model for managing team organization."""
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    team_lead = db.Column(db.String(120))
    project_focus = db.Column(db.String(255))
    max_members = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    members = db.relationship('TeamMember', backref='team', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Team {self.name}>'


class TeamMember(db.Model):
    """Team Member model for managing team membership relationships."""
    __tablename__ = 'team_members'
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False, index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    position = db.Column(db.String(100))  # leader, member, contributor, etc.
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    left_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Composite unique constraint
    __table_args__ = (db.UniqueConstraint('team_id', 'student_id', name='unique_team_member'),)
    
    def __repr__(self):
        return f'<TeamMember Team:{self.team_id} Student:{self.student_id}>'


class Workshop(db.Model):
    """Workshop model for managing workshops and training sessions."""
    __tablename__ = 'workshops'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    instructor = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, index=True)
    end_date = db.Column(db.DateTime)
    location = db.Column(db.String(255))
    capacity = db.Column(db.Integer)
    skill_tags = db.Column(db.String(500))  # comma-separated skills
    status = db.Column(db.String(50), default='scheduled')  # scheduled, ongoing, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    registrations = db.relationship('WorkshopRegistration', backref='workshop', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Workshop {self.title}>'


class WorkshopRegistration(db.Model):
    """Workshop Registration model for managing participant registrations."""
    __tablename__ = 'workshop_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    workshop_id = db.Column(db.Integer, db.ForeignKey('workshops.id'), nullable=False, index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='registered')  # registered, attended, cancelled
    certificate_issued = db.Column(db.Boolean, default=False)
    
    # Composite unique constraint
    __table_args__ = (db.UniqueConstraint('workshop_id', 'student_id', name='unique_workshop_registration'),)
    
    def __repr__(self):
        return f'<WorkshopRegistration Workshop:{self.workshop_id} Student:{self.student_id}>'


class Achievement(db.Model):
    """Achievement model for tracking student achievements and milestones."""
    __tablename__ = 'achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)  # academic, leadership, project, competition, etc.
    date_achieved = db.Column(db.DateTime, nullable=False)
    issuer = db.Column(db.String(120))
    certificate_url = db.Column(db.String(255))
    points = db.Column(db.Integer, default=0)  # gamification points
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Achievement {self.title}>'


class Progress(db.Model):
    """Progress model for tracking student progress and milestones."""
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    metric_name = db.Column(db.String(200), nullable=False)  # e.g., "Workshops Attended", "Events Organized"
    metric_value = db.Column(db.Integer, default=0)
    milestone = db.Column(db.String(200))  # specific milestone description
    status = db.Column(db.String(50), default='in_progress')  # in_progress, completed
    target_value = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Progress {self.metric_name}>'
