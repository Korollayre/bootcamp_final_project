from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
)

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('email', String, nullable=False, unique=True),
    Column('password', String, nullable=False),
    Column('login', String, nullable=False),
    Column('name', String, nullable=True),
    Column('age', String, nullable=True),
)
