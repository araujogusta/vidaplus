from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from vidaplus.models.config.base import Base


class Unit(Base):
    __tablename__ = 'unit'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
