from evraz.classic.http_api import App
from evraz.classic.http_auth import Authenticator

from books_backend.application import services

from . import (
    auth,
    controllers,
)


def create_app(
        books_service: services.BooksManager,

) -> App:
    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)

    authenticator.set_strategies(auth.jwt_strategy)

    app = App(prefix='/api')

    app.register(
        controllers.Books(
            authenticator=authenticator,
            service=books_service,
        )
    )

    return app
