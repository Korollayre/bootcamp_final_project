from unittest.mock import Mock

import pytest

from users_backend.application import interfaces


@pytest.fixture(scope='function')
def users_repo(user):
    users_repo = Mock(interfaces.UsersRepo)
    users_repo.get_all = Mock(return_value=[user])
    users_repo.get_by_id = Mock(return_value=user)
    users_repo.get_by_email = Mock(return_value=None)
    users_repo.add_instance = Mock(return_value=None)
    users_repo.login = Mock(return_value=user)
    return users_repo


@pytest.fixture(scope='function')
def mail_sender():
    mail_sender = Mock(interfaces.MailSender)
    mail_sender.send = Mock(return_value=None)
    return mail_sender
