from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Explicitly specify table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    auth = db.Column(db.String(20), nullable=False, default='user')
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Reference to another user (manager)
    team = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password.decode('utf-8')) if isinstance(generate_password_hash(password), bytes) else generate_password_hash(password)

    # Relationships
    messages_sent = db.relationship('Messages', backref='sender', lazy=True)
    group_chats_created = db.relationship('GroupChatDetails', backref='creator', lazy=True)
    chat_participations = db.relationship('ChatParticipants', backref='participant', lazy=True)

    # Relationship for contacts
    contacts_list = db.relationship('Contacts', foreign_keys='Contacts.user_id', backref='owner', lazy=True)

class Contacts(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # The user who owns the contact list
    contact_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # The user added to contacts
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship for the contact user
    contact = db.relationship('User', foreign_keys=[contact_id])

class Chats(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    is_group = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_archive = db.Column(db.Boolean, default=False)

    # Relationships
    participants = db.relationship('ChatParticipants', backref='chat', lazy=True)
    messages = db.relationship('Messages', backref='chat', lazy=True)
    group_details = db.relationship('GroupChatDetails', uselist=False, backref='chat')  # One-to-one with group details if group

class ChatParticipants(db.Model):
    __tablename__ = 'chat_participants'
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_read_message_id = db.Column(db.Integer, db.ForeignKey('messages.id', use_alter=True, name="fk_last_read_message"))  # Use alter to define this explicitly for reporter DB

    # Relationships with 'overlaps' to avoid conflicts
    user = db.relationship('User', overlaps="chat_participations,participant")
    last_read_message = db.relationship('Messages', foreign_keys=[last_read_message_id])

class GroupChatDetails(db.Model):
    __tablename__ = 'group_chat_details'
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))
    group_name = db.Column(db.String(255), default='New Group')
    group_image = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Reference to the user who created the group
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Messages in Reporter Database
class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))
    content = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

class Reports(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    report_type = db.Column(db.String(50))
    report_time = db.Column(db.DateTime)
    location = db.Column(db.String(20))
    size = db.Column(db.String(255))
    activity = db.Column(db.String(255))
    unit = db.Column(db.String(255))
    equipment = db.Column(db.String(255))
    team = db.Column(db.String(255))
    mission_name = db.Column(db.String(255))
    result = db.Column(db.String(255))  # Typo fixed
    mission_details = db.Column(db.String(1000))
    azimuth = db.Column(db.Float)
    frequency = db.Column(db.Float)
    rssi = db.Column(db.Integer)
    modulation = db.Column(db.String(255))
    technology = db.Column(db.String(255))
    protocol = db.Column(db.String(255))

    # Relationships
    fields = db.relationship('SITREPFields', backref='report', lazy=True)

class SITREPFields(db.Model):
    __tablename__ = 'sitrep_fields'
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'))
    input_type = db.Column(db.String(255))
    input_value = db.Column(db.String(255))
