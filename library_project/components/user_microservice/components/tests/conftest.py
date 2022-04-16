import pytest

from users_backend.application import entities


@pytest.fixture(scope='function')
def user():
    return entities.Users(
        id=1,
        login='SuperDanya',
        email='danya@mail.ru',
        password='password',
        name='Danya',
        age=None,
    )
