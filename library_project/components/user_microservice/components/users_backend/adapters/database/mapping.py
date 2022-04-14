from sqlalchemy.orm import registry

from users_backend.application import entities

from . import tables

mapper = registry()

mapper.map_imperatively(
    entities.Users,
    tables.users
)
