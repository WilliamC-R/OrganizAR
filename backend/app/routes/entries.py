from datetime import date
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from app.schemas.entry import EntrySchema
from app.security.auth import get_current_user, validate_token_version
from app.security.csrf import validate_csrf
from app.services.entry_service import EntryService
from app.utils.responses import error_response, ok_response


entries_bp = Blueprint("entries", __name__)
service = EntryService()
schema = EntrySchema()


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


@entries_bp.get("")
@jwt_required()
def list_entries():
    user = get_current_user()
    invalid = validate_token_version(user)
    if invalid:
        return invalid
    from_date = _parse_date(request.args.get("from"))
    to_date = _parse_date(request.args.get("to"))
    kind = request.args.get("kind")
    category_id = request.args.get("category_id")
    entries = service.list(
        user.id,
        from_date,
        to_date,
        kind,
        int(category_id) if category_id else None,
    )
    return ok_response({"entries": schema.dump(entries, many=True)})


@entries_bp.post("")
@jwt_required()
def create_entry():
    csrf_error = validate_csrf()
    if csrf_error:
        return csrf_error
    user = get_current_user()
    invalid = validate_token_version(user)
    if invalid:
        return invalid
    payload = request.get_json() or {}
    try:
        entry = service.create(
            user_id=user.id,
            category_id=int(payload.get("category_id")),
            kind=payload.get("kind"),
            amount=payload.get("amount"),
            description=payload.get("description"),
            entry_date=date.fromisoformat(payload.get("date")),
        )
    except (TypeError, ValueError):
        return error_response("validation_error", "Invalid entry data"), HTTPStatus.BAD_REQUEST
    return ok_response({"entry": schema.dump(entry)}, HTTPStatus.CREATED)


@entries_bp.put("/<int:entry_id>")
@jwt_required()
def update_entry(entry_id: int):
    csrf_error = validate_csrf()
    if csrf_error:
        return csrf_error
    user = get_current_user()
    invalid = validate_token_version(user)
    if invalid:
        return invalid
    entry = service.repo.get(user.id, entry_id)
    if not entry:
        return error_response("not_found", "Entry not found"), HTTPStatus.NOT_FOUND
    payload = request.get_json() or {}
    try:
        entry = service.update(
            entry,
            category_id=int(payload.get("category_id")),
            kind=payload.get("kind"),
            amount=payload.get("amount"),
            description=payload.get("description"),
            entry_date=date.fromisoformat(payload.get("date")),
        )
    except (TypeError, ValueError):
        return error_response("validation_error", "Invalid entry data"), HTTPStatus.BAD_REQUEST
    return ok_response({"entry": schema.dump(entry)})


@entries_bp.delete("/<int:entry_id>")
@jwt_required()
def delete_entry(entry_id: int):
    csrf_error = validate_csrf()
    if csrf_error:
        return csrf_error
    user = get_current_user()
    invalid = validate_token_version(user)
    if invalid:
        return invalid
    entry = service.repo.get(user.id, entry_id)
    if not entry:
        return error_response("not_found", "Entry not found"), HTTPStatus.NOT_FOUND
    service.delete(entry)
    return ok_response({"ok": True})
