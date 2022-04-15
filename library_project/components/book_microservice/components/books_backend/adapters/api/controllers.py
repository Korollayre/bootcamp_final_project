import os
from typing import List

import jwt

from falcon import (
    Request,
    Response,
)

from evraz.classic.components import component
from evraz.classic.http_auth import (
    authenticate,
    authenticator_needed,
)
from books_backend.application import services

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


def parse_filter_values(filter_value: str) -> List[str]:
    return filter_value.split(':')


@authenticator_needed
@component
class Books:
    service: services.BooksManager

    @join_point
    def on_get_show(self, request: Request, response: Response):
        fields = (
            'title',
            'authors',
            'publisher',
            'price',
        )

        filters_data = {}

        limit = request.get_param_as_int('limit') or 50
        offset = request.get_param_as_int('offset') or 0

        filters_data['limit'] = limit
        filters_data['offset'] = offset

        for field in fields:
            query_data = request.params.get(field)
            if query_data is None:
                filters_data[field] = None
                continue
            field_flag, field_value = parse_filter_values(query_data)
            filters_data[field] = (field_flag, field_value)

        order_by_data = request.params.get('order_by')

        if order_by_data is None:
            filters_data['order_by'] = None
        else:
            filters_data['order_by'] = order_by_data

        books = self.service.get_books(**filters_data)

        response.media = [
            {
                'id': book.isbn13,
                'title': book.title,
                'subtitle': book.subtitle,
                'rating': book.rating,
                'pages': book.pages,
                'price': book.price,
            } for book in books
        ]

    @join_point
    def on_post_info(self, request: Request, response: Response):
        book = self.service.get_book(**request.media)

        response.media = {
            'id': book.isbn13,
            'title': book.title,
            'subtitle': book.subtitle,
            'authors': book.authors,
            'publisher': book.publisher,
            'pages': book.pages,
            'year': book.year,
            'expire_date': book.expire_date.strftime(
                "%Y-%m-%d %H:%M:%S") if book.expire_date is not None else 'Book is free for booking',
            'rating': book.rating,
            'desc': book.desc,
            'price': book.price,
        }

    @join_point
    @authenticate
    def on_post_book(self, request: Request, response: Response):
        user_id = get_user_id_from_token(request)

        day_to_expire = request.media.get('day_to_expire') or 7

        request.media['user_id'] = user_id
        request.media['day_to_expire'] = day_to_expire

        self.service.take_book(**request.media)

        response.media = {
            'message': 'Book successfully booked'
        }

    @join_point
    @authenticate
    def on_post_active(self, request: Request, response: Response):
        user_id = get_user_id_from_token(request)

        request.media['user_id'] = user_id

        book = self.service.check_active_book(**request.media)

        if book is None:
            response.media = {
                'message': 'No active books'
            }
        else:
            response.media = {
                'id': book.isbn13,
                'title': book.title,
                'subtitle': book.subtitle,
                'rating': book.rating,
                'price': book.price,
            }

    @join_point
    @authenticate
    def on_post_bought(self, request: Request, response: Response):
        user_id = get_user_id_from_token(request)

        request.media['user_id'] = user_id

        books = self.service.check_bought_book(**request.media)

        if len(books) == 0:
            response.media = {
                'message': 'No bought books'
            }
        else:
            response.media = [
                {
                    'id': book.isbn13,
                    'title': book.title,
                    'subtitle': book.subtitle,
                    'rating': book.rating,
                    'price': book.price,
                } for book in books
            ]

    @join_point
    @authenticate
    def on_post_buy(self, request: Request, response: Response):
        user_id = get_user_id_from_token(request)

        request.media['user_id'] = user_id

        self.service.buy_book(**request.media)

        response.media = {
            'message': 'Book successfully bought'
        }

    @join_point
    @authenticate
    def on_post_return(self, request: Request, response: Response):
        user_id = get_user_id_from_token(request)

        request.media['user_id'] = user_id

        self.service.return_book(**request.media)

        response.media = {
            'message': 'Book successfully returned'
        }

    @join_point
    @authenticate
    def on_post_user_check(self, request: Request, response: Response):
        user_id = get_user_id_from_token(request)

        request.media['user_id'] = user_id

        history_rows = self.service.check_by_user(**request.media)

        response.media = [
            {
                'id': row.book.isbn13,
                'title': row.book.title,
                'subtitle': row.book.subtitle,
                'rating': row.book.rating,
                'price': row.book.price,
                'created_date': row.created_date.strftime("%Y-%m-%d %H:%M:%S"),
            } for row in history_rows
        ]
