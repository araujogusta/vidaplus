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
    assert response_data['role'] == 'PATIENT'
