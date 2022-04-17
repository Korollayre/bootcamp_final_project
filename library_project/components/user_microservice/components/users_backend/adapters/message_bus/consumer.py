from kombu import Connection

from evraz.classic.messaging_kombu import KombuConsumer

from users_backend.application import services
from .scheme import broker_scheme


def create_consumer(
    connection: Connection,
    users: services.UsersManager,
) -> KombuConsumer:
    consumer = KombuConsumer(
        connection=connection,
        scheme=broker_scheme,
    )

    consumer.register_function(
        users.parse_broker_message,
        'UsersQueue',
    )

    return consumer
