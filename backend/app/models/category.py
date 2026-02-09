from datetime import datetime

from app import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    kind = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="categories")
    entries = db.relationship("Entry", back_populates="category", cascade="all, delete")

    __table_args__ = (db.Index("idx_categories_user_kind", "user_id", "kind"),)
