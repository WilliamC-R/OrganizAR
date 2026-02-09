import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE", "true").lower() == "true"
    JWT_COOKIE_SAMESITE = os.getenv("JWT_COOKIE_SAMESITE", "Strict")
    JWT_COOKIE_CSRF_PROTECT = False
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:4200").split(",")
    ENV = os.getenv("FLASK_ENV", "production")
    PROPAGATE_EXCEPTIONS = True
