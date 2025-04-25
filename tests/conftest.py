from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, StaticPool, create_engine

from vidaplus.main.enums.roles import Roles
from vidaplus.models.config.base import Base
from vidaplus.models.config.connection import DatabaseConnectionHandler
from vidaplus.models.entities.user import User
from vidaplus.run import app
from vidaplus.settings import Settings


@pytest.fixture
def engine(monkeypatch: pytest.MonkeyPatch) -> Generator[Engine, None, None]:
    monkeypatch.setenv('DATABASE_URL', 'sqlite:///:memory:')

    engine = create_engine(Settings().DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool)

    monkeypatch.setattr(DatabaseConnectionHandler, '_DatabaseConnectionHandler__create_engine', lambda x: engine)

    Base.metadata.create_all(engine)

    yield engine

    Base.metadata.drop_all(engine)


@pytest.fixture
def client(engine: Engine) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture
def patient(engine: Engine) -> None:
    user = User(
        name='John Doe',
        email='johndoe@example.com',
        password='ilovepotatos',
        role=Roles.PATIENT,
    )

    with DatabaseConnectionHandler() as db:
        db.session.add(user)
        db.session.commit()
