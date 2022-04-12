from evraz.classic.app.errors import AppError


class FilterKeyError(AppError):
    msg_template = "Unexpected filter key."
    code = 'books_api.filter_key_error'
