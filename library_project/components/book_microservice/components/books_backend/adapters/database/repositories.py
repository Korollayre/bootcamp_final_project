from datetime import datetime
from typing import (
    List,
    Optional, Tuple,
)
from sqlalchemy import (
    and_,
    asc,
    desc,
)

from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository

from books_backend.application import interfaces
from books_backend.application.entities import (
    Books,
    BooksHistory,
)


@component
class BooksRepo(BaseRepository, interfaces.BooksRepo):
    def get_filtered_books(self, text_filters: Tuple, numeric_filters: Tuple, order_by: Optional[str]) -> List[Books]:
        filter_query = []

        for el in text_filters:
            if el is not None:
                filter_query.append(self.get_by_text_filter(el[0], el[1], el[2]))

        for el in numeric_filters:
            if el is not None:
                filter_query.append(self.get_by_numbers_filter(el[0], el[1], el[2]))

        if order_by is None:
            return self.session.query(Books).filter(and_(*filter_query, Books.bought == False)).all()
        else:
            return self.session.query(Books).filter(and_(*filter_query, Books.bought == False)).order_by(
                asc(getattr(Books, order_by))).all()

    def get_by_text_filter(self, field_name: str, filter_flag: str, filter_value: str):
        filters = {
            'like': getattr(Books, field_name).ilike(f'%{filter_value}%'),
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
            desc(Books.rating), asc(Books.year)).limit(3).all()

    def get_by_id(self, book_id: int) -> Optional[Books]:
        return self.session.query(Books).filter_by(isbn13=book_id).one_or_none()

    def add_instance(self, book: Books):
        self.session.add(book)
        self.session.flush()


@component
class HistoryRepo(BaseRepository, interfaces.HistoryRepo):

    def get_by_user_id(self, user_id: int) -> List[BooksHistory]:
        return self.session.query(BooksHistory).filter_by(user_id=user_id).all()

    def get_by_ids(self, book_id: int, user_id: int) -> Optional[BooksHistory]:
        return self.session.query(BooksHistory).filter_by(book_id=book_id, user_id=user_id).order_by(
            desc(BooksHistory.created_date)).limit(1).one_or_none()

    def add_instance(self, new_row: BooksHistory):
        self.session.add(new_row)
        self.session.flush()
