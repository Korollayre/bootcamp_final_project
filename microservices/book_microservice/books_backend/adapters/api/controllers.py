from falcon import (
    Request,
    Response,
)

from evraz.classic.components import component

from books_backend.application import services

from .join_points import join_point


@component
class Books:
    service: services.BooksManager

    @join_point
    def on_get_show(self, request: Request, response: Response):
        books = self.service.get_books()
        response.media = [
            {
                'title': book.title,
                'status': 'Free' if book.user_id is None else 'Busy',
                'subtitle': book.subtitle,
                'authors': book.authors,
                'publisher': book.publisher,
                'pages': book.pages,
                'year': book.year,
                'rating': book.rating,
                'desc': book.desc,
                'price': book.price,
            } for book in books
        ]

    # @join_point
    # def on_post_info(self, request: Request, response: Response):
    #     book = self.service.get_book(**request.media)
    #     response.media = {
    #         'title': book.title,
    #         'author': book.author,
    #         'pages_count': book.pages_count,
    #         'status': 'Free' if book.user_id is None else 'Busy',
    #         'created_date': book.created_date.strftime("%Y-%m-%d %H:%M:%S"),
    #         'modified_date': book.modified_date.strftime("%Y-%m-%d %H:%M:%S"),
    #     }
    #
    # @join_point
    # def on_post_book(self, request: Request, response: Response):
    #     self.service.take_book(**request.media)
    #     response.media = {
    #         'message': 'Book successfully booked'
    #     }
    #
    # @join_point
    # def on_post_return(self, request: Request, response: Response):
    #     self.service.return_book(**request.media)
    #     response.media = {
    #         'message': 'Book successfully returned'
    #     }
    #
    # @join_point
    # def on_post_user_check(self, request: Request, response: Response):
    #     books = self.service.check_by_user(**request.media)
    #     response.media = [
    #         {
    #             'title': book.title,
    #             'author': book.author,
    #             'pages_count': book.pages_count,
    #             'created_date': book.created_date.strftime("%Y-%m-%d %H:%M:%S"),
    #             'modified_date': book.modified_date.strftime("%Y-%m-%d %H:%M:%S"),
    #         } for book in books
    #     ]
    #
    # @join_point
    # def on_post_buy(self, request: Request, response: Response):
    #     self.service.update_book(**request.media)
    #     response.media = {
    #         'message': 'Book info successfully update'
    #     }
