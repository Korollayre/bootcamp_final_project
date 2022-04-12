from sqlalchemy import create_engine

from evraz.classic.sql_storage import TransactionContext

from users_backend.adapters import (
    api,
    database,
)
from users_backend.application import services


class Settings:
    db = database.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine, expire_on_commit=False)

    users_repo = database.repositories.UsersRepo(context=context)


class Application:
    users = services.UsersManager(
        users_repo=DB.users_repo,
    )


class Aspects:
    services.join_points.join(DB.context)
    api.join_points.join(DB.context)


app = api.create_app(
    users_service=Application.users,
)
