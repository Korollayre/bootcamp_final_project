from datetime import datetime
from typing import Optional

import attr


@attr.dataclass
class Books:
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
    created_date: Optional[datetime] = None
    expire_date: Optional[datetime] = None
    bought: Optional[bool] = None


@attr.dataclass
class BooksHistory:
    book_id: Books
    user_id: int
    created_date: Optional[datetime] = None
    id: Optional[int] = None
