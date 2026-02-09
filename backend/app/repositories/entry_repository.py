from datetime import date

from app import db
from app.models.entry import Entry


class EntryRepository:
    def list(
        self,
        user_id: str,
        from_date: date | None = None,
        to_date: date | None = None,
        kind: str | None = None,
        category_id: int | None = None,
    ) -> list[Entry]:
        query = Entry.query.filter_by(user_id=user_id)
        if from_date:
            query = query.filter(Entry.date >= from_date)
        if to_date:
            query = query.filter(Entry.date <= to_date)
        if kind:
            query = query.filter_by(kind=kind)
        if category_id:
            query = query.filter_by(category_id=category_id)
        return query.order_by(Entry.date.desc()).all()

    def get(self, user_id: str, entry_id: int) -> Entry | None:
        return Entry.query.filter_by(user_id=user_id, id=entry_id).first()

    def create(self, entry: Entry) -> Entry:
        db.session.add(entry)
        db.session.commit()
        return entry

    def update(self) -> None:
        db.session.commit()

    def delete(self, entry: Entry) -> None:
        db.session.delete(entry)
        db.session.commit()
