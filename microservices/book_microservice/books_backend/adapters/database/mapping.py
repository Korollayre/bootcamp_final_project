from sqlalchemy.orm import registry

from books_backend.application import entities

from . import tables

mapper = registry()

mapper.map_imperatively(
    entities.Books,
    tables.books_table
)
