from http import HTTPStatus

from fastapi.testclient import TestClient


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


def test_register_new_patient_with_existing_email(client: TestClient, patient: None) -> None:
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
