from evraz.classic.app.errors import AppError


class FilterKeyError(AppError):
    msg_template = "Unexpected filter key."
    code = 'books_api.filter_key_error'


class NoBook(AppError):
    msg_template = "Book with id '{id}' does not exists."
    code = 'book_api.no_book'


class BookedBook(AppError):
    msg_template = "Book with id '{book_id}' already booked."
    code = 'book_api.booked_book'


class BoughtBook(AppError):
    msg_template = "Sorry, but book with id '{book_id}' was bought..."
    code = 'book_api.bought_book'


class NoActiveBook(AppError):
    msg_template = "Oops, you don't have booked book. " \
                   "If you want to buy book, you need to booked it first."
    code = 'book_api.bought_book'


class NoBookedBook(AppError):
    msg_template = "Book with id '{book_id}' not booked by user with id {user_id}."
    code = 'book_api.no_booked_book'


class BookedLimit(AppError):
    msg_template = "You already reading one book. " \
                   "If you want to read one more book, " \
                   "you need to buy or return your previous book."

    code = 'book_api.book_limit'
