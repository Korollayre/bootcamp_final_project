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
    user_id: Optional[int] = None
    booked_date: Optional[datetime] = None
    expire_date: Optional[datetime] = None
    bought: Optional[bool] = None
