import logging

from evraz.classic.components import component

from users_backend.application import interfaces


@component
class StreamMailSender(interfaces.MailSender):
    logger: logging.Logger

    def send(self, user: str, title: str, books: str):
        self.logger.info(
            f'SendTo: {user}\n'
            f'Title: {title}\n'
            f'Body: {books}\n',
        )
