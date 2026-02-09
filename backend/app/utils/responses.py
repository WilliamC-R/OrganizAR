from flask import jsonify


def ok_response(data: dict, status: int = 200):
    return jsonify(data), status


def error_response(code: str, message: str, details: dict | None = None):
    payload = {"error": {"code": code, "message": message}}
    if details:
        payload["error"]["details"] = details
    return jsonify(payload)
