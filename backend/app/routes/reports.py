from datetime import date
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.security.auth import get_current_user, validate_token_version
from app.services.report_service import ReportService
from app.utils.responses import ok_response


reports_bp = Blueprint("reports", __name__)
service = ReportService()


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


@reports_bp.get("/summary")
@jwt_required()
def summary():
    user = get_current_user()
    invalid = validate_token_version(user)
    if invalid:
        return invalid
    from_date = _parse_date(request.args.get("from"))
    to_date = _parse_date(request.args.get("to"))
    data = service.summary(user.id, from_date, to_date)
    return ok_response({"summary": data})
