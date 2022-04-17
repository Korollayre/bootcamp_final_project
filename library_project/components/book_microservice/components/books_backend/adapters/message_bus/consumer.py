from kombu import Connection

from evraz.classic.messaging_kombu import KombuConsumer

from books_backend.application import services
from .scheme import broker_scheme


def create_consumer(
    connection: Connection,
    books: services.BooksManager,
) -> KombuConsumer:
    consumer = KombuConsumer(
        connection=connection,
        scheme=broker_scheme,
    )

    consumer.register_function(
        books.parse_broker_message,
        'BooksQueue',
    )

    return consumer
