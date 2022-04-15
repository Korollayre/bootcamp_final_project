from datetime import datetime
from pydantic import validator
from typing import (
    Optional,
    Tuple,
)

from evraz.classic.app import DTO

from .errors import FilterKeyError


class BooksInfo(DTO):
    isbn13: int
    title: str
    subtitle: str
    authors: str
    publisher: str
    pages: int
    year: int
    rating: int
    desc: str
    price: float
    created_date: datetime
    expire_date: Optional[datetime] = None
    bought: Optional[bool] = None


class BooksInfoForChange(DTO):
    isbn13: int
    title: str
    subtitle: str
    authors: str
    publisher: str
    pages: int
    year: int
    rating: int
    desc: str
    price: float
    created_date: datetime
    expire_date: Optional[datetime] = None
    bought: Optional[bool] = None


class BooksHistoryInfo(DTO):
    book_id: int
    user_id: int
    created_date: datetime


class FiltersInfo(DTO):
    title: Optional[Tuple] = None
    authors: Optional[Tuple] = None
    publisher: Optional[Tuple] = None
    price: Optional[Tuple] = None
    order_by: Optional[str] = None
    limit: int
    offset: int

    @validator('title')
    def title_check(cls, value: Optional[Tuple]) -> Optional[Tuple]:
        if value is None:
            return

        field_flag, field_value = value

        if field_flag not in ('like', 'eq',):
            raise FilterKeyError(
                field='title',
                key=field_flag,
            )

        return 'title', field_flag, field_value

    @validator('authors')
    def authors_check(cls, value: Optional[Tuple]) -> Optional[Tuple]:
        if value is None:
            return

        field_flag, field_value = value

        if field_flag not in ('like', 'eq',):
            raise FilterKeyError(
                field='authors',
                key=field_flag,
            )

        return 'authors', field_flag, field_value

    @validator('publisher')
    def publisher_check(cls, value: Optional[Tuple]) -> Optional[Tuple]:
        if value is None:
            return

        field_flag, field_value = value

        if field_flag not in ('like', 'eq',):
            raise FilterKeyError(
                field='publisher',
                key=field_flag,
            )

        return 'publisher', field_flag, field_value

    @validator('price')
    def price_check(cls, value: Optional[Tuple]) -> Optional[Tuple]:
        if value is None:
            return

        field_flag, field_value = value

        if field_flag not in ('gt', 'gte', 'lt', 'lte',):
            raise FilterKeyError(
                field='price',
                key=field_flag,
            )

        return 'price', field_flag, field_value

    @validator('order_by')
    def order_by_check(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return

        if value not in ('price', 'pages',):
            raise FilterKeyError(
                field=value,
                key='order_by',
            )

        return value
