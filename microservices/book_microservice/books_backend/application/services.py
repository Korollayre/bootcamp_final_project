from datetime import (
    datetime,
    timedelta
)
from typing import (
    List,
    Optional,
)

from evraz.classic.aspects import PointCut
from evraz.classic.components import component
from evraz.classic.messaging import (
    Publisher,
    Message,
)
from pydantic import validate_arguments

from .dto import (
    BooksInfo,
    BooksInfoForChange,
    BooksHistoryInfo,
)
from .errors import (
    NoBook,
    NoActiveBook,
    BoughtBook,
    NoBookedBook,
    BookedBook,
    BookedLimit,
    FilterKeyError,
)
from .entities import (
    Books,
    BooksHistory,
)

from . import interfaces

join_points = PointCut()
join_point = join_points.join_point


@component
class BooksManager:
    books_repo: interfaces.BooksRepo
    history_repo: interfaces.HistoryRepo
    user_publisher: Publisher

    @join_point
    @validate_arguments
    def parse_broker_message(self, api: str, action: str, data: dict):
        with open('books.txt', 'w') as file:
            file.write(f'{action}, {data}')
        if action == 'create':
            book_check = self.books_repo.get_by_id(data['isbn13'])

            if book_check is not None:
                return

            data['price'] = float(data.get('price')[1:])
            book_info = BooksInfo(**data)
            new_book = book_info.create_obj(Books)

            self.books_repo.add_instance(new_book)

        elif action == 'send':

            print('send to user')

            mail_data = {}

            tags = data.get('tags')
            times = data.get('timestamps')

            tags_timestamps = list(zip(tags, times))

            for tag, timestamp in tags_timestamps:
                books = self.books_repo.get_books_for_distribution(timestamp)

                if len(books) == 0:
                    continue

                mail_data[f'{tag}'] = [
                    {
                        'id': book.isbn13,
                        'title': book.title,
                        'subtitle': book.subtitle,
                        'rating': book.rating,
                        'year': book.year,
                        'price': book.price,
                    } for book in books
                ]

            if len(mail_data.keys()) == 0:
                return

            self.user_publisher.publish(
                Message(
                    'result',
                    {
                        'api': 'books',
                        'action': 'send',
                        'data': mail_data,
                    }
                )
            )

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

    @join_point
    @validate_arguments
    def get_book(self, book_id: int) -> Books:
        book = self.books_repo.get_by_id(book_id)

        if book is None:
            raise NoBook(id=book_id)

        return book

    @join_point
    @validate_arguments
    def take_book(self, book_id: int, user_id: int, day_to_expire: Optional[int]):
        book = self.get_book(book_id)

        if book.expire_date is not None and book.expire_date > datetime.today():
            raise BookedBook(book_id=book_id)

        if book.bought is True:
            raise BoughtBook(book_id=book_id)

        book_history = self.check_by_user(user_id)
        for row in book_history:
            if row.book.expire_date is None:
                continue
            if row.book.expire_date > datetime.today():
                raise BookedLimit()

        history_info = BooksHistoryInfo(
            book_id=book_id,
            user_id=user_id,
            created_date=datetime.now(),
        )

        new_history_row = history_info.create_obj(BooksHistory)

        self.history_repo.add_instance(new_history_row)

        new_expire_date = datetime.today() + timedelta(day_to_expire if day_to_expire <= 7 else 7)

        book_info = BooksInfoForChange(
            isbn13=book.isbn13,
            title=book.title,
            subtitle=book.subtitle,
            authors=book.authors,
            publisher=book.publisher,
            pages=book.pages,
            year=book.year,
            rating=book.rating,
            desc=book.desc,
            price=book.price,
            created_date=book.created_date,
            expire_date=new_expire_date,
            bought=book.bought,
        )

        book_info.populate_obj(book)

    @join_point
    @validate_arguments
    def check_active_book(self, user_id: int) -> Optional[Books]:
        history_rows = self.history_repo.get_by_user_id(user_id)
        for row in history_rows:
            if row.book.expire_date is not None:
                if row.book.expire_date > datetime.today():
                    return row.book

    @join_point
    @validate_arguments
    def check_bought_book(self, user_id: int) -> List[Books]:
        history_rows = self.history_repo.get_by_user_id(user_id)
        books = []
        for row in history_rows:
            if row.book.bought is True:
                if row.book not in books:
                    books.append(row.book)

        return books

    @join_point
    @validate_arguments
    def buy_book(self, user_id: int):
        active_book = self.check_active_book(user_id)

        if active_book is None:
            raise NoActiveBook()

        book_info = BooksInfoForChange(
            isbn13=active_book.isbn13,
            title=active_book.title,
            subtitle=active_book.subtitle,
            authors=active_book.authors,
            publisher=active_book.publisher,
            pages=active_book.pages,
            year=active_book.year,
            rating=active_book.rating,
            desc=active_book.desc,
            price=active_book.price,
            created_date=active_book.created_date,
            expire_date=None,
            bought=True,
        )

        book_info.populate_obj(active_book)

    @join_point
    @validate_arguments
    def return_book(self, book_id: int, user_id: int):
        book = self.get_book(book_id)

        book_history = self.history_repo.get_by_ids(book_id=book_id, user_id=user_id)

        if book_history is None:
            raise NoBookedBook(user_id=user_id, book_id=book_id)

        if book_history.book.expire_date < datetime.today():
            return

        book_info = BooksInfoForChange(
            isbn13=book.isbn13,
            title=book.title,
            subtitle=book.subtitle,
            authors=book.authors,
            publisher=book.publisher,
            pages=book.pages,
            year=book.year,
            rating=book.rating,
            desc=book.desc,
            price=book.price,
            created_date=book.created_date,
            expire_date=None,
            bought=book.bought,
        )

        book_info.populate_obj(book)

    @join_point
    @validate_arguments
    def check_by_user(self, user_id: int) -> List[BooksHistory]:
        books = self.history_repo.get_by_user_id(user_id)

        return books
