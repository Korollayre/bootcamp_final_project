import os

import jwt

from falcon import Request, Response

from evraz.classic.components import component
from evraz.classic.http_auth import (
    authenticate,
    authenticator_needed,
)
from users_backend.application import services

from .join_points import join_point


def get_user_id_from_token(request: Request):
    str_token = request.get_header('AUTHORIZATION').split()[1]
    bytes_token = str.encode(str_token)
    token_data = jwt.decode(
        bytes_token,
        key=os.getenv('SECRET_JWT_KEY'),
        algorithms='HS256',
    )

    return token_data.get('sub')

@authenticator_needed
@component
class Users:
    service: services.UsersManager

    @join_point
    def on_post_register(self, request: Request, response: Response):
        self.service.create_user(**request.media)
        response.media = {
            'message': 'User registration completed successfully'
        }

    @join_point
    def on_post_login(self, request: Request, response: Response):
        user = self.service.login(**request.media)
        response.set_header(
            'auth_token',
            jwt.encode(
                {
                    'sub': user.id,
                    'login': user.login,
                    'name': user.name,
                    'group': 'User',
                    'email': user.email,
                },
                key=os.getenv('SECRET_JWT_KEY'),
                algorithm='HS256',
            ),
        )
        response.media = {
            'message': 'Login complete successful'
        }

    @join_point
    @authenticate
    def on_get_logout(self, request: Request, response: Response):
        response.set_header('auth_token', 'empty token')
        response.media = {
            'message': 'Logout complete successful'
        }

    @join_point
    @authenticate
    def on_get_show_user(self, request: Request, response: Response):
        user_id = get_user_id_from_token(request)

        request.params['user_id'] = user_id

        user = self.service.get_user(**request.params)
        response.media = {
            'email': user.email,
            'login': user.login,
            'name': user.name,
            'age': user.age,
        }
