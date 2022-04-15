from datetime import datetime, timedelta

from pydantic import ValidationError
from unittest.mock import Mock

import pytest

from books_backend.application.services import BooksManager
from books_backend.application.errors import (
    NoBook,
    NoActiveBook,
    BoughtBook,
    NoBookedBook,
    BookedBook,
    BookedLimit,
)


@pytest.fixture(scope='function')
def book_service(books_repo, history_repo, user_publisher):
    return BooksManager(
        books_repo=books_repo,
        history_repo=history_repo,
        user_publisher=user_publisher,
    )


parse_broker_message__valid_cases = [
    {
        'api': 'books',
        'action': 'create',
        'data': {
            'isbn13': 'book_info'
        },
    },
    {
        'api': 'books',
        'action': 'send',
        'data': {
            'tags': [
                'tag_1',
                'tag_2',
            ],
            'timestamps': [
                'time_1',
                'time_2',
            ],
        },
    }
]


@pytest.mark.parametrize('test_cases', parse_broker_message__valid_cases)
def test__parse_broker_message(test_cases, book_service, books_repo):
    assert book_service.parse_broker_message(**test_cases) is None


parse_broker_message__invalid_cases = [
    {
        'api': 'books',
        'action': 'create',
    },
    {
        'api': 'books',
        'data': {
            'isbn13': 'book_info'
        },
    },
    {
        'action': 'create',
        'data': {
            'isbn13': 'book_info'
        },
    },
    {
        'api': 'books',
        'action': 'create',
        'data': 111,
    },
    {

    },
]


@pytest.mark.parametrize('test_cases', parse_broker_message__invalid_cases)
def test__parse_broker_message__missing_arguments(book_service, test_cases):
    with pytest.raises(ValidationError):
        book_service.parse_broker_message(**test_cases)


def test__get_book(book_service, book_2):
    case_data = {
        'book_id': 9781449303211,
    }

    assert book_service.get_book(**case_data) == book_2


get_book__invalid_cases = [
    {
        'book_id': 'aaaaaaaaa',
    },
    {
        'book_id': 9781449303211,
        'extra_field': 'data',
    },
    {

    },
]


@pytest.mark.parametrize('test_cases', get_book__invalid_cases)
def test__get_book__missing_arguments(book_service, test_cases):
    with pytest.raises(ValidationError):
        book_service.get_book(**test_cases)


def test__get_book__invalid_book_id(book_service, books_repo):
    case_data = {
        'book_id': 3,
    }

    books_repo.get_by_id = Mock(return_value=None)

    with pytest.raises(NoBook):
        book_service.get_book(**case_data)


def test__get_books(book_service, book_1, book_2):
    case_data = {
        'limit': 50,
        'offset': 0,
    }
    assert book_service.get_books(**case_data) == [book_1, book_2]


def test__take_book(book_service):
    case_data = {
        'book_id': 628316291631,
        'user_id': 1,
        'day_to_expire': 7,
    }

    assert book_service.take_book(**case_data) is None


take_book__invalid_cases = [
    {
        'user_id': 1,
        'day_to_expire': 7,
    },
    {
        'book_id': 628316291631,
        'day_to_expire': 7,
    },
    {
        'book_id': 628316291631,
        'user_id': 1,
    },
    {
        'book_id': 628316291631,
        'user_id': 1,
        'day_to_expire': 'ssssssssssss',
    },
    {
        'book_id': 628316291631,
        'user_id': 1,
        'day_to_expire': 7,
        'extra_field': 'data',
    },
    {

    },
]


@pytest.mark.parametrize('test_cases', take_book__invalid_cases)
def test__take_book__missing_arguments(book_service, test_cases):
    with pytest.raises(ValidationError):
        book_service.take_book(**test_cases)


def test__take_book__booked_book(book_service, books_repo, booked_book):
    case_data = {
        'book_id': 628316291631,
        'user_id': 1,
        'day_to_expire': 7,
    }

    books_repo.get_by_id = Mock(return_value=booked_book)

    with pytest.raises(BookedBook):
        book_service.take_book(**case_data)


def test__take_book__bought_book(book_service, books_repo, bought_book):
    case_data = {
        'book_id': 628316291631,
        'user_id': 1,
        'day_to_expire': 7,
    }

    books_repo.get_by_id = Mock(return_value=bought_book)

    with pytest.raises(BoughtBook):
        book_service.take_book(**case_data)


def test__take_book__booked_limit(book_service, history_repo, book_history_with_booked_book):
    case_data = {
        'book_id': 628316291631,
        'user_id': 1,
        'day_to_expire': 7,
    }

    book_history_with_booked_book.book.expire_date = datetime.today() + timedelta(8)

    history_repo.get_by_user_id = Mock(return_value=[book_history_with_booked_book])

    with pytest.raises(BookedLimit):
        book_service.take_book(**case_data)


def test__check_active_book(book_service, history_repo, book_history_with_booked_book):
    case_data = {
        'user_id': 1,
    }

    history_repo.get_by_user_id = Mock(return_value=[book_history_with_booked_book])

    assert book_service.check_active_book(**case_data) == book_history_with_booked_book.book


check_active_book__invalid_cases = [
    {
        'book_id': 628316291631,
    },
    {
        'user_id': 1,
        'extra_field': 'data',
    },
    {

    },
]


@pytest.mark.parametrize('test_cases', check_active_book__invalid_cases)
def test__check_active_book__missing_arguments(book_service, test_cases):
    with pytest.raises(ValidationError):
        book_service.check_active_book(**test_cases)


def test__check_bought_book(book_service, history_repo, book_history_with_bought_book, bought_book):
    case_data = {
        'user_id': 1,
    }

    history_repo.get_by_user_id = Mock(return_value=[book_history_with_bought_book])

    assert book_service.check_bought_book(**case_data) == [bought_book]


check_bought_book__invalid_cases = [
    {
        'book_id': 628316291631,
    },
    {
        'user_id': 1,
        'extra_field': 'data',
    },
    {

    },
]


@pytest.mark.parametrize('test_cases', check_bought_book__invalid_cases)
def test__check_bought_book__missing_arguments(book_service, test_cases):
    with pytest.raises(ValidationError):
        book_service.check_bought_book(**test_cases)


def test__buy_book(book_service, history_repo, book_history_with_booked_book):
    case_data = {
        'user_id': 1,
    }

    history_repo.get_by_user_id = Mock(return_value=[book_history_with_booked_book])

    assert book_service.buy_book(**case_data) is None


buy_book__invalid_cases = [
    {
        'book_id': 1,
    },
    {
        'user_id': 1,
        'extra_field': 'data',
    },
    {

    },
]


@pytest.mark.parametrize('test_cases', buy_book__invalid_cases)
def test__buy_book__missing_arguments(book_service, test_cases):
    with pytest.raises(ValidationError):
        book_service.buy_book(**test_cases)


def test__buy_book__no_active_book(book_service):
    case_data = {
        'user_id': 1,
    }
    with pytest.raises(NoActiveBook):
        assert book_service.buy_book(**case_data) is None


def test__return_book(book_service, books_repo, booked_book, history_repo, book_history_with_booked_book):
    case_data = {
        'book_id': 628316291631,
        'user_id': 1,
    }

    books_repo.get_by_id = Mock(return_value=booked_book)

    history_repo.get_by_ids = Mock(return_value=book_history_with_booked_book)

    assert book_service.return_book(**case_data) is None


return_book__invalid_cases = [
    {
        'book_id': 628316291631,
    },
    {
        'user_id': 1,
    },
    {
        'book_id': 'aaaaaaaaa',
    },
    {
        'book_id': 628316291631,
        'user_id': 1,
        'extra_field': 'data',
    },
    {

    },
]


@pytest.mark.parametrize('test_cases', return_book__invalid_cases)
def test__return_book__missing_arguments(book_service, test_cases):
    with pytest.raises(ValidationError):
        book_service.return_book(**test_cases)


def test__return_book__no_booked_book(book_service, history_repo):
    case_data = {
        'book_id': 628316291631,
        'user_id': 1,
    }

    history_repo.get_by_ids = Mock(return_value=None)

    with pytest.raises(NoBookedBook):
        book_service.return_book(**case_data)
