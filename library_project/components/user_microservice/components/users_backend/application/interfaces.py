from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Optional,
    List,
)

from .entities import Users


class UsersRepo(ABC):
    @abstractmethod
    def get_all(self) -> List[Users]:
        ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[Users]:
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Users]:
        ...

    @abstractmethod
    def add_instance(self, user: Users):
        ...

    @abstractmethod
    def login(self, user_mail: str, user_password: str) -> Optional[Users]:
        ...


class MailSender(ABC):
    @abstractmethod
    def send(self, user: str, title: str, data: str):
        ...
