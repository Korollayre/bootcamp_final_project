import pytest

from unittest.mock import Mock

from evraz.classic.messaging import Publisher

from books_backend.application import interfaces


@pytest.fixture(scope='function')
def books_repo(book_1, book_2):
    books_repo = Mock(interfaces.BooksRepo)
    books_repo.get_filtered_books = Mock(return_value=[book_1, book_2])
    books_repo.get_by_text_filter = Mock(return_value=None)
    books_repo.get_by_numbers_filter = Mock(return_value=None)
    books_repo.get_books_for_distribution = Mock(return_value=[book_1])
    books_repo.get_by_id = Mock(return_value=book_2)
    books_repo.get_by_user = Mock(return_value=book_1)
    books_repo.add_instance = Mock(return_value=None)
    return books_repo


@pytest.fixture(scope='function')
def history_repo(book_history_1, book_history_2):
    history_repo = Mock(interfaces.HistoryRepo)
    history_repo.get_by_user_id = Mock(return_value=[book_history_1])
    history_repo.get_by_ids = Mock(return_value=book_history_2)
    history_repo.add_instance = Mock(return_value=None)
    return history_repo


@pytest.fixture(scope='function')
def user_publisher():
    user_publisher = Mock(Publisher)
    user_publisher.publish = Mock(return_value=None)
    return user_publisher
