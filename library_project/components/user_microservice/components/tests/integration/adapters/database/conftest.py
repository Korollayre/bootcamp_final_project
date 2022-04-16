import datetime
import os
import pytest

from sqlalchemy import create_engine

from evraz.classic.sql_storage import TransactionContext

from users_backend.adapters.database.tables import metadata


@pytest.fixture(scope='session')
def engine():
    test_db_url: str = f"{os.getenv('DB_DRIVER')}://" \
                       f"{os.getenv('DB_USER')}:" \
                       f"{os.getenv('DB_PASSWORD')}@" \
                       f"{os.getenv('DB_HOST')}:" \
                       f"{os.getenv('DB_PORT')}/" \
                       f"{os.getenv('DB_TEST_DATABASE')}"

    engine = create_engine(test_db_url)

    for key, value in metadata.tables.items():
        value.schema = None

    metadata.create_all(engine)

    return engine


@pytest.fixture(scope='session')
def transaction_context(engine):
    return TransactionContext(bind=engine)


@pytest.fixture(scope='function')
def session(transaction_context: TransactionContext):
    session = transaction_context.current_session

    if session.in_transaction():
        session.begin_nested()
    else:
        session.begin()

    yield session

    session.rollback()
