from sqlalchemy import select

from vidaplus.main.schemas.user import CreateUserSchema, UserSchema
from vidaplus.models.config.connection import DatabaseConnectionHandler
from vidaplus.models.entities.user import User
from vidaplus.models.repositories.interfaces.user_repository_interface import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    def create(self, new_user: CreateUserSchema) -> UserSchema:
        with DatabaseConnectionHandler() as db:
            try:
                user = User(**new_user.model_dump())
                db.session.add(user)
                db.session.commit()
                db.session.refresh(user)
                return UserSchema.model_validate(user)
            except Exception as ex:
                db.session.rollback()
                raise ex

    def get_by_email(self, email: str) -> UserSchema | None:
        with DatabaseConnectionHandler() as db:
            try:
                user = db.session.scalar(select(User).where(User.email == email))

                return UserSchema.model_validate(user) if user else None
            except Exception as ex:
                db.session.rollback()
                raise ex
