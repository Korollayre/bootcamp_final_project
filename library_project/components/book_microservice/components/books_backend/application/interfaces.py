from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
    Optional,
    Tuple,
)

from .entities import (
    Books,
    BooksHistory,
)


class BooksRepo(ABC):
    @abstractmethod
    def get_filtered_books(self, text_filters: Tuple, numeric_filters: Tuple, order_by: Optional[str]) -> List[Books]:
        ...

    @abstractmethod
    def get_by_text_filter(self, field_name: str, filter_flag: str, filter_value: str):
        ...

    @abstractmethod
    def get_by_numbers_filter(self, field_name: str, filter_flag: str, filter_value: str):
        ...

    @abstractmethod
    def get_books_for_distribution(self, filter_value: str) -> List[Books]:
        ...

    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Books]:
        ...

    @abstractmethod
    def get_by_user(self, user_id: int) -> List[Books]:
        ...

    @abstractmethod
    def add_instance(self, book: Books):
        ...


class HistoryRepo(ABC):
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[BooksHistory]:
        ...

    @abstractmethod
    def get_by_ids(self, book_id: int, user_id: int) -> Optional[BooksHistory]:
        ...

    @abstractmethod
    def add_instance(self, new_row: BooksHistory):
        ...
