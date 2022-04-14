from evraz.classic.app.errors import AppError


class UserRegistration(AppError):
    msg_template = "User with email {email} already exist"
    code = 'chat.user_exist'


class NoUser(AppError):
    msg_template = "User with entered data does not exist"
    code = 'chat.no_user'
