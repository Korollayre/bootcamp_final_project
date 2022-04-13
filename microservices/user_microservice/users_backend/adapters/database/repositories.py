from typing import (
    Optional,
    List,
)

from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository

from users_backend.application import interfaces
from users_backend.application.entities import Users


@component
class UsersRepo(BaseRepository, interfaces.UsersRepo):
    def get_all(self) -> List[Users]:
        return self.session.query(Users).all()

    def get_by_id(self, user_id: int) -> Optional[Users]:
        return self.session.query(Users).filter(Users.id == user_id).one_or_none()

    def get_by_email(self, email: str) -> Optional[Users]:
        return self.session.query(Users).filter(Users.email == email).one_or_none()

    def add_instance(self, user: Users):
        self.session.add(user)
        self.session.flush()

    def login(self, user_mail: str, user_password: str) -> Optional[Users]:
        return self.session.query(Users).filter(Users.email == user_mail, Users.password == user_password).one_or_none()
