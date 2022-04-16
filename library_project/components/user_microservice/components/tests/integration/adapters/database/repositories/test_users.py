import pytest

from sqlalchemy.orm import registry

from users_backend.adapters.database import (
    tables,
    repositories,
)
from users_backend.application.entities import Users


@pytest.fixture(scope='function')
def fill_db(session):
    users_data = [
        {
            'id': 1,
            'login': 'SuperDanya',
            'email': 'danya@mail.ru',
            'password': 'password',
            'name': 'Danya',
            'age': None,
        },
        {
            'id': 2,
            'login': 'MegaMisha',
            'email': 'misha@mail.ru',
            'password': 'password',
            'name': 'Misha',
            'age': None,
        },
    ]

    session.execute(tables.users.insert(), users_data)


@pytest.fixture(scope='function')
def mapper():
    mapper = registry()
    mapper.map_imperatively(Users, tables.users)


@pytest.fixture(scope='function')
def user_repo(transaction_context):
    return repositories.UsersRepo(context=transaction_context)


def test__get_by_id(user_repo, fill_db, first_user):
    test_case = {
        'user_id': 1,
    }
    assert first_user == user_repo.get_by_id(**test_case)


def test__get_all(user_repo, fill_db, first_user, second_user):
    assert [first_user, second_user] == user_repo.get_all()


def test__get_by_email(user_repo, fill_db, second_user):
    test_case = {
        'email': 'misha@mail.ru',
    }

    assert second_user == user_repo.get_by_email(**test_case)


def test__login(user_repo, fill_db, first_user):
    test_case = {
        'user_mail': 'danya@mail.ru',
        'user_password': 'password',
    }

    assert first_user == user_repo.login(**test_case)


def test__add_instance(user_repo, fill_db):
    test_case = {
        'id': 3,
        'email': 'vasya@mail.ru',
        'password': 'password',
        'login': 'KiloVasya',
        'name': 'Vasya',
    }

    assert user_repo.add_instance(Users(**test_case)) is None
