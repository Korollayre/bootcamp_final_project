from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    DateTime,
    BigInteger,
    Boolean,
    Float,
)

metadata = MetaData()

books_table = Table(
    'books',
    metadata,
    Column('isbn13', BigInteger, primary_key=True),
    Column('title', String(500)),
    Column('subtitle', String(500)),
    Column('authors', String(500)),
    Column('publisher', String(500)),
    Column('pages', Integer),
    Column('year', Integer),
    Column('rating', Integer),
    Column('pages', Integer),
    Column('desc', String(500)),
    Column('price', Float),
    Column('user_id', Integer, default=None),
    Column('created_date', DateTime, nullable=False),
    Column('booked_date', DateTime, default=None),
    Column('expire_date', DateTime, default=None),
    Column('bought', Boolean, default=False),
)
