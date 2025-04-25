from vidaplus.main.enums.roles import Roles
from vidaplus.main.exceptions import EmailAlreadyExistsError
from vidaplus.main.schemas.user import CreateUserSchema, PublicUserSchema, RequestCreateUserSchema
from vidaplus.models.repositories.interfaces.user_repository_interface import UserRepositoryInterface


class UserService:
    def __init__(self, repository: UserRepositoryInterface) -> None:
        self.repository = repository

    def new_patient(self, new_user: RequestCreateUserSchema) -> PublicUserSchema:
        try:
            email_already_exists = self.repository.get_by_email(new_user.email)

            if email_already_exists:
                raise EmailAlreadyExistsError()

            user_with_role = CreateUserSchema(**new_user.model_dump(), role=Roles.PATIENT)
            created_user = self.repository.create(user_with_role)
            return PublicUserSchema(**created_user.model_dump())
        except Exception as e:
            raise e
