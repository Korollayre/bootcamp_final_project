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
    ForeignKey,
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
    Column('desc', String(500)),
    Column('price', Float),
    Column('created_date', DateTime, nullable=False),
    Column('expire_date', DateTime, default=None),
    Column('bought', Boolean, default=False),
)

history_table = Table(
    'history',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', BigInteger, ForeignKey('books.isbn13')),
    Column('user_id', Integer),
    Column('created_date', DateTime, nullable=False),
)
