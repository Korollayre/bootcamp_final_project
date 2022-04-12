from books_backend.adapters.cli import create_cli
from books_backend.composites.api import MessageBus

cli = create_cli(MessageBus.publisher)
