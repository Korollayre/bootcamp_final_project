from sqlalchemy.orm import (
    registry,
    relationship,
)

from books_backend.application import entities

from . import tables

mapper = registry()

mapper.map_imperatively(entities.Books, tables.books_table)

mapper.map_imperatively(
    entities.BooksHistory,
    tables.history_table,
    properties={'book': relationship(entities.Books, backref='history')},
)
