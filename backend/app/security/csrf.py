from flask import request
from http import HTTPStatus
from app.utils.responses import error_response


CSRF_COOKIE_NAME = "csrf_token"
CSRF_HEADER_NAME = "X-CSRF-Token"


def validate_csrf() -> tuple[dict, int] | None:
    cookie_token = request.cookies.get(CSRF_COOKIE_NAME)
    header_token = request.headers.get(CSRF_HEADER_NAME)
    if not cookie_token or not header_token or cookie_token != header_token:
        return error_response("csrf_failed", "Invalid CSRF token"), HTTPStatus.FORBIDDEN
    return None
