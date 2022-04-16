import pytest

from falcon import testing
from unittest.mock import Mock

from users_backend.adapters import api
from users_backend.application import services


@pytest.fixture(scope='function')
def user_service_for_controllers(user):
    user_service = Mock(services.UsersManager)
    user_service.create_user = Mock(return_value=None)
    user_service.login = Mock(return_value=user)
    user_service.get_user = Mock(return_value=user)

    return user_service


@pytest.fixture(scope='function')
def client(user_service_for_controllers):
    app = api.create_app(
        users_service=user_service_for_controllers,
    )

    return testing.TestClient(app)
