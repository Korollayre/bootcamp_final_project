from kombu import (
    Exchange,
    Queue,
)

from evraz.classic.messaging_kombu import BrokerScheme

broker_scheme = BrokerScheme(
    Queue(
        'BooksQueue',
        Exchange('APIExchange'),
        routing_key='init',
        max_length=10
    ),
)
