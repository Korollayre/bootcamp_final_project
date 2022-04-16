import pytest

from falcon import testing
from unittest.mock import Mock

from books_backend.adapters import api
from books_backend.application import services


@pytest.fixture(scope='function')
def book_service_for_controllers(
        book_1,
        book_2,
        booked_book,
        bought_book,
        book_history_with_booked_book,
        book_history_with_bought_book,
):
    book_service_for_controllers = Mock(services.BooksManager)
    book_service_for_controllers.get_books = Mock(return_value=[book_1, book_2])
    book_service_for_controllers.get_book = Mock(return_value=book_1)
    book_service_for_controllers.take_book = Mock(return_value=None)
    book_service_for_controllers.check_active_book = Mock(return_value=booked_book)
    book_service_for_controllers.check_bought_book = Mock(return_value=[bought_book])
    book_service_for_controllers.buy_book = Mock(return_value=None)
    book_service_for_controllers.return_book = Mock(return_value=None)
    book_service_for_controllers.check_by_user = Mock(return_value=[book_history_with_booked_book])

    return book_service_for_controllers


@pytest.fixture(scope='function')
def client(book_service_for_controllers):
    app = api.create_app(
        books_service=book_service_for_controllers,
    )

    return testing.TestClient(app)
