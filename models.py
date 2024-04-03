from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.mapped_column(db.Integer, primary_key=True)
    username = db.mapped_column(db.String(50), unique=True)
    # SECURITY NOTE: Don't actually store passwords like this in a real system!
    password = db.mapped_column(db.String(80))

    def __str__(self):
        return self.username

class Timestamp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Float, nullable=False)
    # Add any other necessary columns
