from evraz.classic.http_api import App

from books_backend.application import services

from . import controllers


def create_app(
        books_service: services.BooksManager,

) -> App:
    app = App(prefix='/api')

    app.register(controllers.Books(service=books_service))

    return app
