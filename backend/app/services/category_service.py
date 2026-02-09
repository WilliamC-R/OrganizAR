from app.models.category import Category
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def list(self, user_id: str, kind: str | None):
        return self.repo.list(user_id, kind)

    def create(self, user_id: str, name: str, kind: str) -> Category:
        category = Category(user_id=user_id, name=name, kind=kind)
        return self.repo.create(category)

    def update(self, category: Category, name: str, kind: str) -> Category:
        category.name = name
        category.kind = kind
        self.repo.update()
        return category

    def delete(self, category: Category) -> None:
        self.repo.delete(category)
