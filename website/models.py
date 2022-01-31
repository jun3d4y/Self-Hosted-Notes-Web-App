from flask_login import UserMixin
from datetime import datetime

from .__init__ import db

class User(UserMixin, db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    notes = db.relationship('Note', backref='user', lazy=True)

class Note(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    string_id = db.Column(db.String(30), unique=True)
    title = db.Column(db.String(100), default="New note")
    content = db.Column(db.String(100), default="Type your text here...")
    hash = db.Column(db.String(32), default="ca032621c95c37100071bcbff4dd9926")
    modification_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
