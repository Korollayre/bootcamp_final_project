from kombu import Connection
from sqlalchemy import create_engine

from evraz.classic.sql_storage import TransactionContext

from users_backend.adapters import (
    database,
    message_bus,
)
from users_backend.application import services


class Settings:
    db = database.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine, expire_on_commit=False)

    users_repo = database.repositories.UsersRepo(context=context)


class Application:
    users = services.UsersManager(
        users_repo=DB.users_repo,
    )


class MessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)
    consumer = message_bus.create_consumer(connection, Application.users)

    @staticmethod
    def declare_scheme():
        message_bus.broker_scheme.declare(MessageBus.connection)


if __name__ == '__main__':
    MessageBus.declare_scheme()
    MessageBus.consumer.run()
