from app import db
from app.models.category import Category


class CategoryRepository:
    def list(self, user_id: str, kind: str | None = None) -> list[Category]:
        query = Category.query.filter_by(user_id=user_id)
        if kind:
            query = query.filter_by(kind=kind)
        return query.order_by(Category.created_at.desc()).all()

    def get(self, user_id: str, category_id: int) -> Category | None:
        return Category.query.filter_by(user_id=user_id, id=category_id).first()

    def create(self, category: Category) -> Category:
        db.session.add(category)
        db.session.commit()
        return category

    def update(self) -> None:
        db.session.commit()

    def delete(self, category: Category) -> None:
        db.session.delete(category)
        db.session.commit()
