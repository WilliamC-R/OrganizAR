import uuid
from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    token_version = db.Column(db.Integer, default=0, nullable=False)

    categories = db.relationship("Category", back_populates="user", cascade="all, delete")
    entries = db.relationship("Entry", back_populates="user", cascade="all, delete")
