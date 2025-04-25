from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from vidaplus.main.enums.roles import Roles


class RequestCreateUserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class CreateUserSchema(RequestCreateUserSchema):
    role: Roles


class UserSchema(CreateUserSchema):
    id: UUID
    created_at: datetime


class PublicUserSchema(UserSchema):
    password: str = Field(exclude=True)
