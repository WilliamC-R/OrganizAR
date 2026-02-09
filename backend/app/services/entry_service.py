from datetime import date

from app.models.entry import Entry
from app.repositories.entry_repository import EntryRepository


class EntryService:
    def __init__(self):
        self.repo = EntryRepository()

    def list(
        self,
        user_id: str,
        from_date: date | None,
        to_date: date | None,
        kind: str | None,
        category_id: int | None,
    ):
        return self.repo.list(user_id, from_date, to_date, kind, category_id)

    def create(
        self,
        user_id: str,
        category_id: int,
        kind: str,
        amount,
        description: str | None,
        entry_date: date,
    ) -> Entry:
        entry = Entry(
            user_id=user_id,
            category_id=category_id,
            kind=kind,
            amount=amount,
            description=description,
            date=entry_date,
        )
        return self.repo.create(entry)

    def update(
        self,
        entry: Entry,
        category_id: int,
        kind: str,
        amount,
        description: str | None,
        entry_date: date,
    ) -> Entry:
        entry.category_id = category_id
        entry.kind = kind
        entry.amount = amount
        entry.description = description
        entry.date = entry_date
        self.repo.update()
        return entry

    def delete(self, entry: Entry) -> None:
        self.repo.delete(entry)
