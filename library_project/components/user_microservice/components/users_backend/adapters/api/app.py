from evraz.classic.http_api import App
from evraz.classic.http_auth import Authenticator

from users_backend.application import services

from . import (
    auth,
    controllers,
)


def create_app(users_service: services.UsersManager, ) -> App:
    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)

    authenticator.set_strategies(auth.jwt_strategy)

    app = App(prefix='/api')

    app.register(
        controllers.Users(
            authenticator=authenticator,
            service=users_service,
        )
    )

    return app
