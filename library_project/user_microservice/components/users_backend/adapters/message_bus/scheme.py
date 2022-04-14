from kombu import (
    Exchange,
    Queue,
)

from evraz.classic.messaging_kombu import BrokerScheme

broker_scheme = BrokerScheme(
    Queue(
        'UsersQueue',
        Exchange('APIExchange'),
        routing_key='distribution',
        max_length=10
    ),
)
