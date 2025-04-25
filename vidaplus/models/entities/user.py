from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from vidaplus.main.enums.roles import Roles
from vidaplus.models.config.base import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Roles] = mapped_column(Enum(Roles), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
