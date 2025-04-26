from http import HTTPStatus

from fastapi.testclient import TestClient

from vidaplus.main.enums.roles import Roles
from vidaplus.main.schemas.user import UserSchema


def test_create_healcare_professional(client: TestClient, admin: UserSchema, admin_token: str) -> None:
    data = {
        'name': 'Jane Doe',
        'email': 'janedoe@example.com',
        'password': 'ilovestrawberries',
    }

    response = client.post('/api/profissionais', json=data, headers={'Authorization': f'Bearer {admin_token}'})
    response_data = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert response_data['name'] == data['name']
    assert response_data['email'] == data['email']
    assert response_data['role'] == Roles.HEALTHCARE_PROFESSIONAL
    assert 'id' in response_data
    assert 'created_at' in response_data
    assert 'password' not in response_data


def test_create_healcare_professional_without_token(client: TestClient) -> None:
    data = {
        'name': 'Jane Doe',
        'email': 'janedoe@example.com',
        'password': 'ilovestrawberries',
    }

    response = client.post('/api/profissionais', json=data)
    response_data = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response_data['detail'] == 'Not authenticated'


def test_create_healcare_professional_another_role(client: TestClient, token: str) -> None:
    data = {
        'name': 'Jane Doe',
        'email': 'janedoe@example.com',
        'password': 'ilovestrawberries',
    }

    response = client.post('/api/profissionais', json=data, headers={'Authorization': f'Bearer {token}'})
    response_data = response.json()

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response_data['detail'] == 'Você não tem permissão para acessar este recurso'
