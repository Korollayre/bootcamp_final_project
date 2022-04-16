import pytest

from users_backend.application import entities


@pytest.fixture(scope='function')
def first_user():
    return entities.Users(
        id=1,
        login='SuperDanya',
        email='danya@mail.ru',
        password='password',
        name='Danya',
        age=None,
    )


@pytest.fixture(scope='function')
def second_user():
    return entities.Users(
        id=2,
        login='MegaMisha',
        email='misha@mail.ru',
        password='password',
        name='Misha',
        age=None,
    )
