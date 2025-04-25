from typing import Generator

from fastapi.testclient import TestClient
import pytest

from vidaplus.run import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
