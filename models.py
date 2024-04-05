from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from decimal import Decimal

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.mapped_column(db.Integer, primary_key=True)
    firstname = db.mapped_column(db.String(50))
    surname = db.mapped_column(db.String(50))
    email = db.mapped_column(db.String(50), unique=True)
    # SECURITY NOTE: Don't actually store passwords like this in a real system!
    password = db.mapped_column(db.String(80))

    def __str__(self):
        return self.email

class Timestamp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Float, nullable=False)
    # Add any other necessary columns

class MatchDetails(db.Model):
    
    id = db.mapped_column(db.Integer, primary_key=True)
    home_team = db.mapped_column(db.String(30), nullable=False)
    away_team = db.mapped_column(db.String(30), nullable=False)
    youtube_link = db.mapped_column(db.Text, nullable=False)
    venue = db.mapped_column(db.Text, nullable=False)
    videoid = db.mapped_column(db.Text, nullable=False)
    home_score = db.mapped_column(db.Integer, nullable=False)
    away_score = db.mapped_column(db.Integer, nullable=False)
    match_date = db.mapped_column(db.DateTime, nullable=False)
    competition = db.mapped_column(db.Text, nullable=False)
    created_at = db.mapped_column(db.DateTime, default=datetime.utcnow)
    author_id = db.mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('match_details', lazy=True))


class MatchClips(db.Model):
    id = db.mapped_column(db.Integer, primary_key=True)
    code = db.mapped_column(db.String(30), nullable=False)
    timestamp = db.mapped_column(db.Numeric, nullable=False)
    browser_id = db.mapped_column(db.String(50), nullable=False)
    match_id = db.mapped_column(db.Integer, db.ForeignKey('match_details.id'), nullable=False)
    match = db.relationship('MatchDetails', backref=db.backref('match_clips', lazy=True))

    def serialize(self):

        return {'id': self.id,
        'code': self.code,
        'time': str(self.timestamp) if isinstance(self.timestamp, Decimal) else self.timestamp,
        'browser_id':self.browser_id,
        'match_id':self.match_id
        }

