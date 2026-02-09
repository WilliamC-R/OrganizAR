from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    jwt_required,
)
from http import HTTPStatus

from app.schemas.user import UserSchema
from app.services.auth_service import AuthService
from app.security.auth import get_current_user, validate_token_version
from app.utils.responses import error_response, ok_response


auth_bp = Blueprint("auth", __name__)
user_schema = UserSchema()
service = AuthService()


def _set_csrf_cookie(response, csrf_token: str):
    options = service.csrf_cookie_options()
    response.set_cookie(options["key"], csrf_token, httponly=options["httponly"], secure=options["secure"], samesite=options["samesite"])


@auth_bp.post("/register")
def register():
    payload = request.get_json() or {}
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        return error_response("validation_error", "Email and password required"), HTTPStatus.BAD_REQUEST
    existing = service.user_repo.get_by_email(email)
    if existing:
        return error_response("email_taken", "Email already registered"), HTTPStatus.BAD_REQUEST
    user = service.register(email, password)
    return ok_response({"user": user_schema.dump(user)}, HTTPStatus.CREATED)


@auth_bp.post("/login")
def login():
    payload = request.get_json() or {}
    email = payload.get("email")
    password = payload.get("password")
    user = service.authenticate(email, password)
    if not user:
        return error_response("invalid_credentials", "Invalid credentials"), HTTPStatus.UNAUTHORIZED
    access_token, refresh_token, csrf_token = service.create_tokens(user)
    response = jsonify({"user": user_schema.dump(user)})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    _set_csrf_cookie(response, csrf_token)
    return response


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    user = get_current_user()
    invalid = validate_token_version(user)
    if invalid:
        return invalid
    access_token, csrf_token = service.refresh_access(user)
    response = jsonify({"ok": True})
    set_access_cookies(response, access_token)
    _set_csrf_cookie(response, csrf_token)
    return response


@auth_bp.post("/logout")
@jwt_required()
def logout():
    user = get_current_user()
    if user:
        service.logout(user)
    response = jsonify({"ok": True})
    unset_jwt_cookies(response)
    response.delete_cookie("csrf_token")
    return response


@auth_bp.get("/me")
@jwt_required()
def me():
    user = get_current_user()
    invalid = validate_token_version(user)
    if invalid:
        return invalid
    return ok_response({"user": user_schema.dump(user)})
