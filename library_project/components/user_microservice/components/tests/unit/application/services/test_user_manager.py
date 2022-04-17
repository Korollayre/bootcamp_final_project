from pydantic import ValidationError
from unittest.mock import Mock

import pytest

from users_backend.application.services import UsersManager
from users_backend.application.errors import (
    UserRegistration,
    NoUser,
)


@pytest.fixture(scope='function')
def users_service(users_repo, mail_sender):
    return UsersManager(
        users_repo=users_repo,
        mail_sender=mail_sender,
    )


def test__parse_broker_message(users_service, users_repo):
    case_data = {
        'api': 'some_api',
        'action': 'send',
        'data': {
            'tag_1': [
                'book_1',
                'book_2',
            ]
        },
    }

    assert users_service.parse_broker_message(**case_data) is None


parse_broker_message__invalid_cases = [
    {
        'api': 'some_api',
        'action': 'send',
    },
    {
        'api': 'some_api',
        'data': {
            'tag_1': [
                'book_1',
                'book_2',
            ]
        },
    },
    {
        'action': 'send',
        'data': {
            'tag_1': [
                'book_1',
                'book_2',
            ]
        },
    },
    {
        'api': 'some_api',
        'action': 'send',
        'data': 111
    },
    {},
]


@pytest.mark.parametrize('test_cases', parse_broker_message__invalid_cases)
def test__parse_broker_message__missing_arguments(users_service, test_cases):
    with pytest.raises(ValidationError):
        users_service.parse_broker_message(**test_cases)


create_user__valid_cases = [
    {
        'email': 'example@mail.ru',
        'password': 'password',
        'login': 'some_logic',
        'name': 'some_name',
    },
    {
        'email': 'example@mail.ru',
        'password': 'password',
        'login': 'some_logic',
        'name': 'some_name',
        'age': 22,
    },
]


@pytest.mark.parametrize('test_cases', create_user__valid_cases)
def test__create_user(users_service, test_cases):
    assert users_service.create_user(**test_cases) is None


create_user__invalid_cases = [
    {
        'password': 'password',
        'login': 'some_logic',
        'name': 'some_name',
    },
    {
        'email': 'example@mail.ru',
        'login': 'some_logic',
        'name': 'some_name',
    },
    {
        'email': 'example@mail.ru',
        'password': 'password',
        'name': 'some_name',
    },
    {
        'email': 'example@mail.ru',
        'password': 'password',
        'login': 'some_logic',
    },
    {
        'email': 'example@mail.ru',
        'password': 'password',
        'login': 'some_logic',
        'name': 'some_name',
        'age': 'bbbbbbbbbbb',
    },
    {},
]


@pytest.mark.parametrize('test_cases', create_user__invalid_cases)
def test__create_book__missing_arguments(users_service, test_cases):
    with pytest.raises(ValidationError):
        users_service.create_user(**test_cases)


def test__create_user__invalid_username(users_service, users_repo, user):
    case_data = {
        'email': 'example@mail.ru',
        'password': 'password',
        'login': 'some_logic',
        'name': 'some_name',
    }

    users_repo.get_by_email = Mock(return_value=user)

    with pytest.raises(UserRegistration):
        users_service.create_user(**case_data)


def test__get_user(users_service, user):
    case_data = {
        'user_id': 1,
    }

    assert users_service.get_user(**case_data) == user


get_user_invalid_cases = [
    {
        'user_id': 'aaaaaaaaa',
    },
    {
        'user_id': 1,
        'extra_field': 'data',
    },
    {},
]


@pytest.mark.parametrize('test_cases', get_user_invalid_cases)
def test__get_user__missing_arguments(users_service, test_cases):
    with pytest.raises(ValidationError):
        users_service.get_user(**test_cases)


def test__get_user__invalid_user_id(users_service, users_repo):
    case_data = {
        'user_id': 3,
    }

    users_repo.get_by_id = Mock(return_value=None)

    with pytest.raises(NoUser):
        users_service.get_user(**case_data)


def test__login(users_service, user):
    case_data = {
        'email': 'example@mail.ru',
        'password': 'password',
    }

    assert users_service.login(**case_data) == user


login_invalid_cases = [
    {
        'email': 'example@mail.ru',
    },
    {
        'password': 'password',
    },
    {
        'email': 'example@mail.ru',
        'password': 'password',
        'extra_field': 'data',
    },
    {},
]


@pytest.mark.parametrize('test_cases', login_invalid_cases)
def test__login__missing_arguments(users_service, test_cases):
    with pytest.raises(ValidationError):
        users_service.login(**test_cases)


login_invalid_data_cases = [
    {
        'email': 'bad_email',
        'password': 'password',
    },
    {
        'email': 'example@mail.ru',
        'password': 'bad_password',
    },
]


@pytest.mark.parametrize('test_cases', login_invalid_data_cases)
def test__login__invalid_email(users_service, users_repo, test_cases):
    users_repo.login = Mock(return_value=None)
    with pytest.raises(NoUser):
        users_service.login(**test_cases)
