import uuid
from datetime import datetime
from flask import current_app
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.security.csrf import CSRF_COOKIE_NAME


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register(self, email: str, password: str) -> User:
        password_hash = generate_password_hash(password).decode("utf-8")
        user = User(email=email, password_hash=password_hash, created_at=datetime.utcnow())
        return self.user_repo.create(user)

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        if not check_password_hash(user.password_hash, password):
            return None
        return user

    def create_tokens(self, user: User):
        additional_claims = {"token_version": user.token_version}
        access_token = create_access_token(
            identity=user.id, additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(
            identity=user.id, additional_claims=additional_claims
        )
        csrf_token = uuid.uuid4().hex
        return access_token, refresh_token, csrf_token

    def refresh_access(self, user: User):
        additional_claims = {"token_version": user.token_version}
        access_token = create_access_token(
            identity=user.id, additional_claims=additional_claims
        )
        csrf_token = uuid.uuid4().hex
        return access_token, csrf_token

    def logout(self, user: User) -> None:
        self.user_repo.increment_token_version(user)

    @staticmethod
    def csrf_cookie_options():
        return {
            "key": CSRF_COOKIE_NAME,
            "httponly": False,
            "secure": current_app.config["JWT_COOKIE_SECURE"],
            "samesite": current_app.config["JWT_COOKIE_SAMESITE"],
        }
