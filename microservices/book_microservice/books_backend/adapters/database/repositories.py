from typing import (
    List,
    Optional,
)

from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository

from books_backend.application import interfaces
from books_backend.application.entities import Books


@component
class BooksRepo(BaseRepository, interfaces.BooksRepo):
    def add_instance(self, book: Books):
        self.session.add(book)
        self.session.flush()
        self.session.refresh(book)
        return book

    def get_by_id(self, book_id: int) -> Optional[Books]:
        return self.session.query(Books).filter_by(id=book_id).one_or_none()

    def get_by_title(self, title_for_check: str) -> Optional[Books]:
        return self.session.query(Books).filter_by(title=title_for_check).one_or_none()

    def get_by_user(self, user_id: int) -> Optional[Books]:
        return self.session.query(Books).filter_by(user_id=user_id).all()

    def get_all(self) -> List[Books]:
        return self.session.query(Books).all()

    def delete_instance(self, book: Books):
        self.session.delete(book)
        self.session.flush()
