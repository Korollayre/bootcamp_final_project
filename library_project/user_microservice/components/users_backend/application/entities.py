from typing import Optional

import attr


@attr.dataclass
class Users:
    email: str
    password: str
    login: str
    name: str
    id: Optional[int] = None
    age: Optional[int] = None
