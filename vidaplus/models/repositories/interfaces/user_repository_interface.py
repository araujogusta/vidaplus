from abc import ABC, abstractmethod

from vidaplus.main.schemas.user import CreateUserSchema, UserSchema


class UserRepositoryInterface(ABC):
    @abstractmethod
    def create(self, new_user: CreateUserSchema) -> UserSchema:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> UserSchema | None:
        pass
