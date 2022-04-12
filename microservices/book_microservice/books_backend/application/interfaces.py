from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
    Optional,
)

from .entities import Books


class BooksRepo(ABC):
    @abstractmethod
    def add_instance(self, user: Books) -> Books:
        ...

    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Books]:
        ...

    @abstractmethod
    def get_by_title(self, title_for_check: str) -> Optional[Books]:
        ...

    @abstractmethod
    def get_by_user(self, user_id: int) -> List[Books]:
        ...

    @abstractmethod
    def get_all(self) -> List[Books]:
        ...
