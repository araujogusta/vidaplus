from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy import select

from vidaplus.main.schemas.user import UserSchema
from vidaplus.models.config.connection import DatabaseConnectionHandler
from vidaplus.models.entities.user import User


def test_register_new_patient(client: TestClient) -> None:
    data = {
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'password': 'ilovepotatos',
    }

    response = client.post('/api/pacientes', json=data)
    response_data = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert response_data['name'] == data['name']
    assert response_data['email'] == data['email']
    assert 'password' not in response_data
    assert 'role' in response_data
    assert 'id' in response_data
    assert 'created_at' in response_data
    assert response_data['role'] == 'PATIENT'


def test_register_new_patient_with_existing_email(client: TestClient, patient: UserSchema) -> None:
    data = {
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'password': 'ilovepotatos',
    }

    response = client.post('/api/pacientes', json=data)
    response_data = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_data['detail'] == 'O email já foi cadastrado'


def test_register_new_patient_with_invalid_email(client: TestClient) -> None:
    data = {
        'name': 'John Doe',
        'email': 'johndoe',
        'password': 'ilovepotatos',
    }

    response = client.post('/api/pacientes', json=data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_patient_password_is_hashed(client: TestClient, patient: UserSchema) -> None:
    with DatabaseConnectionHandler() as db:
        user_data = db.session.scalar(select(User).where(User.email == patient.email))

    assert user_data is not None
    assert user_data.password != patient.password
    assert patient.verify_password(user_data.password)
