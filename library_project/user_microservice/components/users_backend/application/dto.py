from typing import Optional

from evraz.classic.app import DTO


class UsersInfo(DTO):
    email: str
    password: str
    login: str
    name: str
    id: Optional[int]
    age: Optional[int]
