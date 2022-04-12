from typing import Optional

from sqlalchemy import select

from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository

from users_backend.application import interfaces
from users_backend.application.entities import Users


@component
class UsersRepo(BaseRepository, interfaces.UsersRepo):
    def get_by_id(self, user_id: int) -> Optional[Users]:
        query = select(Users).where(Users.id == user_id)
        return self.session.execute(query).scalars().one_or_none()

    def get_by_email(self, email: str) -> Optional[Users]:
        query = select(Users).where(Users.email == email)
        return self.session.execute(query).scalars().one_or_none()

    def add_instance(self, user: Users):
        self.session.add(user)
        self.session.flush()

    def login(self, user_mail: str, user_password: str) -> Users:
        query = select(Users).where(Users.email == user_mail, Users.password == user_password)
        return self.session.execute(query).scalars().one_or_none()
