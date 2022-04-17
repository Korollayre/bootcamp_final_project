import os

from evraz.classic.http_auth import (
    Group,
    Permission,
    strategies,
)


class Permissions:
    FULL_CONTROL = Permission('full_control')


class Groups:
    ADMINS = Group(
        'admins',
        permissions=(Permissions.FULL_CONTROL, ),
    )


jwt_strategy = strategies.JWT(secret_key=os.getenv('SECRET_JWT_KEY'), )

ALL_GROUPS = (Groups.ADMINS, )
