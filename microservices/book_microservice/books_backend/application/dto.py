from datetime import datetime
from typing import Optional

from evraz.classic.app import DTO


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
