from datetime import datetime
from typing import (
    List,
    Optional,
)
from sqlalchemy import (
    and_,
    asc,
    desc,
)

from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository

from books_backend.application import interfaces
from books_backend.application.entities import Books


@component
class BooksRepo(BaseRepository, interfaces.BooksRepo):
    def get_filtered_books(self, filter_query: List, order_by_field: Optional[str]) -> List[Books]:
        if order_by_field is None:
            return self.session.query(Books).filter(and_(*filter_query)).all()
        else:
            return self.session.query(Books).filter(and_(*filter_query)).order_by(
                asc(getattr(Books, order_by_field))).all()

    def get_by_text_filter(self, field_name: str, filter_flag: str, filter_value: str):
        filters = {
            'like': getattr(Books, field_name).like(f'%{filter_value}%'),
            'eq': getattr(Books, field_name) == filter_value,
        }
        return filters.get(filter_flag)

    def get_by_numbers_filter(self, field_name: str, filter_flag: str, filter_value: str):
        filters = {
            'gt': getattr(Books, field_name) > filter_value,
            'gte': getattr(Books, field_name) >= filter_value,
            'lt': getattr(Books, field_name) < filter_value,
            'lte': getattr(Books, field_name) <= filter_value,
        }
        return filters.get(filter_flag)

    def get_books_for_distribution(self, timestamp: datetime) -> List[Books]:
        return self.session.query(Books).filter_by(created_date=timestamp).order_by(
            desc(Books.rating), desc(Books.year)).limit(3).all()

    def get_by_id(self, book_id: int) -> Optional[Books]:
        return self.session.query(Books).filter_by(isbn13=book_id).one_or_none()

    def get_by_user(self, user_id: int) -> Optional[Books]:
        return self.session.query(Books).filter_by(user_id=user_id).all()

    def add_instance(self, book: Books):
        self.session.add(book)
        self.session.flush()
