from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from app.schemas.category import CategorySchema
from app.security.auth import get_current_user, validate_token_version
from app.security.csrf import validate_csrf
from app.services.category_service import CategoryService
from app.utils.responses import error_response, ok_response


categories_bp = Blueprint("categories", __name__)
service = CategoryService()
schema = CategorySchema()


@categories_bp.get("")
@jwt_required()
def list_categories():
    user = get_current_user()
    invalid = validate_token_version(user)
    if invalid:
        return invalid
    kind = request.args.get("kind")
    categories = service.list(user.id, kind)
    return ok_response({"categories": schema.dump(categories, many=True)})


@categories_bp.post("")
@jwt_required()
def create_category():
    csrf_error = validate_csrf()
    if csrf_error:
        return csrf_error
    user = get_current_user()
    invalid = validate_token_version(user)
    if invalid:
        return invalid
    payload = request.get_json() or {}
    name = payload.get("name")
    kind = payload.get("kind")
    if not name or kind not in {"income", "expense"}:
        return error_response("validation_error", "Name and kind required"), HTTPStatus.BAD_REQUEST
    category = service.create(user.id, name, kind)
    return ok_response({"category": schema.dump(category)}, HTTPStatus.CREATED)


@categories_bp.put("/<int:category_id>")
@jwt_required()
def update_category(category_id: int):
    csrf_error = validate_csrf()
    if csrf_error:
        return csrf_error
    user = get_current_user()
    invalid = validate_token_version(user)
    if invalid:
        return invalid
    category = service.repo.get(user.id, category_id)
    if not category:
        return error_response("not_found", "Category not found"), HTTPStatus.NOT_FOUND
    payload = request.get_json() or {}
    name = payload.get("name")
    kind = payload.get("kind")
    if not name or kind not in {"income", "expense"}:
        return error_response("validation_error", "Name and kind required"), HTTPStatus.BAD_REQUEST
    category = service.update(category, name, kind)
    return ok_response({"category": schema.dump(category)})


@categories_bp.delete("/<int:category_id>")
@jwt_required()
def delete_category(category_id: int):
    csrf_error = validate_csrf()
    if csrf_error:
        return csrf_error
    user = get_current_user()
    invalid = validate_token_version(user)
    if invalid:
        return invalid
    category = service.repo.get(user.id, category_id)
    if not category:
        return error_response("not_found", "Category not found"), HTTPStatus.NOT_FOUND
    service.delete(category)
    return ok_response({"ok": True})
