from pydantic import validate_arguments

from evraz.classic.app import validate_with_dto
from evraz.classic.aspects import PointCut
from evraz.classic.components import component

from . import interfaces
from .dto import UsersInfo
from .entities import Users
from .errors import NoUser, UserRegistration

join_points = PointCut()
join_point = join_points.join_point


@component
class UsersManager:
    users_repo: interfaces.UsersRepo
    mail_sender: interfaces.MailSender

    @join_point
    @validate_arguments
    def parse_broker_message(self, api: str, action: str, data: dict):
        if action == 'send':
            users = self.users_repo.get_all()
            for tag in data.keys():
                books = data.get(tag)
                for user in users:
                    self.mail_sender.send(
                        user.email,
                        f'The best selection of {tag} books just for you!',
                        books,
                    )

    @join_point
    @validate_with_dto
    def create_user(self, user_info: UsersInfo):
        email_check = self.users_repo.get_by_email(email=user_info.email)

        if email_check is not None:
            raise UserRegistration(email=user_info.email)

        new_user = user_info.create_obj(Users)
        self.users_repo.add_instance(new_user)

    @join_point
    @validate_arguments
    def login(self, email: str, password: str) -> Users:
        user = self.users_repo.login(user_mail=email, user_password=password)
        if user is None:
            raise NoUser()
        return user

    @join_point
    @validate_arguments
    def get_user(self, user_id: int) -> Users:
        user = self.users_repo.get_by_id(user_id)
        if user is None:
            raise NoUser()
        return user
