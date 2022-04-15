import pytest

from users_backend.application import entities


@pytest.fixture
def user():
    return entities.Users(
        id=1,
        login='UserLogin',
        email='UserEmail',
        name='UserName',
        password='password',
        age=22,
    )
