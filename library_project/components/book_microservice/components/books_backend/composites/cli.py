from books_backend.adapters.cli import create_cli
from books_backend.composites.api import (
    PublisherMessageBus,
    ConsumerMessageBus,
)

cli = create_cli(PublisherMessageBus.book_publisher, ConsumerMessageBus)
