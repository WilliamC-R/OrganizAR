from datetime import date
from sqlalchemy import func

from app import db
from app.models.entry import Entry


class ReportService:
    def summary(self, user_id: str, from_date: date | None, to_date: date | None):
        base_query = Entry.query.filter_by(user_id=user_id)
        if from_date:
            base_query = base_query.filter(Entry.date >= from_date)
        if to_date:
            base_query = base_query.filter(Entry.date <= to_date)

        totals = (
            base_query.with_entities(Entry.kind, func.sum(Entry.amount))
            .group_by(Entry.kind)
            .all()
        )
        totals_map = {kind: float(total or 0) for kind, total in totals}

        by_category = (
            base_query.with_entities(Entry.category_id, func.sum(Entry.amount))
            .group_by(Entry.category_id)
            .all()
        )

        by_month = (
            base_query.with_entities(
                func.date_trunc("month", Entry.date).label("month"),
                Entry.kind,
                func.sum(Entry.amount),
            )
            .group_by("month", Entry.kind)
            .order_by("month")
            .all()
        )

        return {
            "totals": {
                "income": totals_map.get("income", 0),
                "expense": totals_map.get("expense", 0),
                "net": totals_map.get("income", 0) - totals_map.get("expense", 0),
            },
            "by_category": [
                {"category_id": category_id, "total": float(total or 0)}
                for category_id, total in by_category
            ],
            "by_month": [
                {
                    "month": month.isoformat(),
                    "kind": kind,
                    "total": float(total or 0),
                }
                for month, kind, total in by_month
            ],
        }
