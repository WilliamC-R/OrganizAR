from flask_jwt_extended import get_jwt_identity, get_jwt
from http import HTTPStatus

from app.repositories.user_repository import UserRepository
from app.utils.responses import error_response


user_repo = UserRepository()


def get_current_user():
    user_id = get_jwt_identity()
    if not user_id:
        return None
    return user_repo.get_by_id(user_id)


def validate_token_version(user) -> tuple[dict, int] | None:
    token_version = get_jwt().get("token_version")
    if user is None or token_version != user.token_version:
        return error_response("token_revoked", "Token revoked"), HTTPStatus.UNAUTHORIZED
    return None
