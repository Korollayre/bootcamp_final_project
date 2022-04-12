from datetime import datetime
from typing import (
    List,
    Optional, Union,
)

from evraz.classic.app import (
    DTO,
    validate_with_dto,
)
from evraz.classic.aspects import PointCut
from evraz.classic.components import component
from evraz.classic.messaging import (
    Publisher,
    Message,
)
from pydantic import validate_arguments

from .errors import (
    # NoBook,
    # BookExists,
    # NoRights,
    # BookedBook,
    FilterKeyError,
)
from .entities import Books

from . import interfaces

join_points = PointCut()
join_point = join_points.join_point


class BooksInfo(DTO):
    isbn13: int
    title: str
    subtitle: str
    authors: str
    publisher: str
    pages: int
    year: int
    rating: int
    pages: int
    desc: str
    price: float
    user_id: Optional[int] = None
    booked_date: Optional[datetime] = None
    expire_date: Optional[datetime] = None
    bought: Optional[bool] = None


@component
class BooksManager:
    books_repo: interfaces.BooksRepo
    user_publisher: Publisher

    @join_point
    @validate_arguments
    def parse_broker_message(self, api: str, action: str, data: Union[dict, tuple]):
        if action == 'create':

            data['price'] = float(data.get('price')[1:])
            book_info = BooksInfo(**data)
            new_book = book_info.create_obj(Books)

            self.books_repo.add_instance(new_book)

        elif action == 'send':
            mail_data = {}

            for tag in data:

                mail_data[f'{tag}'] = None
                pass

    @join_point
    @validate_arguments
    def get_book(self, book_id: int) -> Books:
        book = self.books_repo.get_by_id(book_id)

        if book is None:
            raise NoBook(id=book_id)

        return book

    @join_point
    def get_books(self, query: dict) -> List[Books]:
        books = self.filter_books(query)

        return books

    @join_point
    @validate_arguments
    def filter_books(self, query: dict) -> Optional[List[Books]]:
        filter_query = []

        header_filter = query.get('title')
        if header_filter is not None:
            flag, value = self.parse_filter_values(header_filter)
            filter_query.append(self.filter_by_text_filters('title', flag, value))

        header_filter = query.get('authors')
        if header_filter is not None:
            flag, value = self.parse_filter_values(header_filter)
            filter_query.append(self.filter_by_text_filters('authors', flag, value))

        text_filter = query.get('publisher')
        if text_filter is not None:
            flag, value = self.parse_filter_values(text_filter)
            filter_query.append(self.filter_by_text_filters('publisher', flag, value))

        likes_filters = query.get('price')
        if likes_filters is not None:
            flag, value = self.parse_filter_values(likes_filters)
            filter_query.append(self.filter_by_numbers_filters('price', flag, value))

        order_by_field = query.get('order_by')
        if order_by_field in ('price', 'pages', None):
            books = self.books_repo.get_filtered_books(filter_query, order_by_field)
        else:
            raise FilterKeyError()

        limit = query.get('limit')
        offset = query.get('offset')

        return books[offset: limit + offset]

    @staticmethod
    def parse_filter_values(filter_value: str) -> List[str]:
        return filter_value.split(':')

    def filter_by_text_filters(self, field_name: str, filter_flag: str, filter_value: str):
        filter_query = self.books_repo.get_by_text_filter(field_name, filter_flag, filter_value)

        if filter_query is None:
            raise FilterKeyError()

        return filter_query

    def filter_by_numbers_filters(self, field_name: str, filter_flag: str, filter_value: str):
        filter_query = self.books_repo.get_by_numbers_filter(field_name, filter_flag, filter_value)

        if filter_query is None:
            raise FilterKeyError()

        return filter_query

    # @join_point
    # @validate_arguments
    # def take_book(self, book_id: int, user_id: int):
    #     book = self.get_book(book_id)
    #
    #     if book.user_id is not None:
    #         raise BookedBook(book_id=book_id)
    #
    #     book_info = BooksInfoForChange(
    #         book_id=book_id,
    #         title=book.title,
    #         pages_count=book.pages_count,
    #         author=book.author,
    #         user_id=user_id,
    #     )
    #
    #     book_info.populate_obj(book)
    #
    #     book_info.book_id = book_id
    #
    #     self.publisher.plan(
    #         Message(
    #             'result',
    #             {
    #                 'api': 'books',
    #                 'action': 'take',
    #                 'data': book_info.dict(),
    #             }
    #         )
    #     )
    #
    # @join_point
    # @validate_arguments
    # def return_book(self, book_id: int, user_id: int):
    #     book = self.get_book(book_id)
    #
    #     if book.user_id != user_id:
    #         raise NoRights(user_id=user_id, book_id=book_id)
    #
    #     book_info = BooksInfoForChange(
    #         book_id=book_id,
    #         title=book.title,
    #         pages_count=book.pages_count,
    #         author=book.author,
    #         user_id=None,
    #     )
    #
    #     book_info.populate_obj(book)
    #
    #     book_info.book_id = book_id
    #
    #     self.publisher.plan(
    #         Message(
    #             'result',
    #             {
    #                 'api': 'books',
    #                 'action': 'return',
    #                 'data': book_info.dict(),
    #             }
    #         )
    #     )
    #
    # @join_point
    # @validate_arguments
    # def check_by_user(self, user_id: int) -> List[Books]:
    #     return self.books_repo.get_by_user(user_id)
    #
    # @join_point
    # @validate_with_dto
    # def update_book(self, book_info: BooksInfoForChange):
    #     if book_info.title is not None:
    #         self.check_title(book_info.title)
    #
    #     book = self.get_book(book_info.book_id)
    #
    #     book.modified_date = datetime.now()
    #     if book_info.title is not None:
    #         book.title = book_info.title
    #     book.author = book_info.author
    #     book.pages_count = book_info.pages_count
    #
    #     book_info.populate_obj(book)
    #
    # @join_point
    # @validate_with_dto
    # def partially_update_book(self, book_info: BooksInfoForChange):
    #     if book_info.title is not None:
    #         self.check_title(book_info.title)
    #
    #     book = self.get_book(book_info.book_id)
    #
    #     book.modified_date = datetime.now()
    #
    #     book_info.populate_obj(book)
    #
    # @join_point
    # @validate_arguments
    # def delete_book(self, book_id: int):
    #     book = self.get_book(book_id)
    #
    #     self.books_repo.delete_instance(book)
    #
    #     self.publisher.plan(
    #         Message(
    #             'result',
    #             {
    #                 'api': 'books',
    #                 'action': 'delete',
    #                 'data': {'book_id': book_id},
    #             }
    #         )
    #     )
