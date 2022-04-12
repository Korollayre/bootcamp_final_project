from kombu import Connection
from sqlalchemy import create_engine

from evraz.classic.messaging_kombu import KombuPublisher
from evraz.classic.sql_storage import TransactionContext

from books_backend.adapters import (
    api,
    database,
    message_bus,
)
from books_backend.application import services


class Settings:
    db = database.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine, expire_on_commit=False)

    books_repo = database.repositories.BooksRepo(context=context)


class MessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
        messages_params={
            'result': {
                'exchange': 'APIExchange',
                'routing_key': 'init',
            }
        },
    )


class Application:
    books = services.BooksManager(books_repo=DB.books_repo)


class Aspects:
    services.join_points.join(
        MessageBus.publisher,
        DB.context,
    )
    api.join_points.join(DB.context)


app = api.create_app(
    books_service=Application.books,
)
