from http import HTTPStatus
from flask import Flask, jsonify


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPStatus.BAD_REQUEST)
    def bad_request(error):
        return _error("bad_request", str(error)), HTTPStatus.BAD_REQUEST

    @app.errorhandler(HTTPStatus.UNAUTHORIZED)
    def unauthorized(error):
        return _error("unauthorized", str(error)), HTTPStatus.UNAUTHORIZED

    @app.errorhandler(HTTPStatus.FORBIDDEN)
    def forbidden(error):
        return _error("forbidden", str(error)), HTTPStatus.FORBIDDEN

    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found(error):
        return _error("not_found", str(error)), HTTPStatus.NOT_FOUND

    @app.errorhandler(Exception)
    def internal_error(error):
        return _error("server_error", "Unexpected error"), HTTPStatus.INTERNAL_SERVER_ERROR


def _error(code: str, message: str, details: dict | None = None):
    payload = {"error": {"code": code, "message": message}}
    if details:
        payload["error"]["details"] = details
    return jsonify(payload)
