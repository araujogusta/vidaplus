import random
from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi.testclient import TestClient

from vidaplus.main.enums.appointment_status import AppointmentStatus
from vidaplus.main.enums.appointment_types import AppointmentTypes
from vidaplus.main.schemas.user import UserSchema


def test_create_appointment(
    client: TestClient, patient: UserSchema, healthcare_profissional: UserSchema, token: str, date_in_future: str
) -> None:
    data = {
        'patient_id': str(patient.id),
        'professional_id': str(healthcare_profissional.id),
        'date_time': date_in_future,
        'type': AppointmentTypes.CONSULTATION,
        'status': AppointmentStatus.SCHEDULED,
        'estimated_duration': random.randint(1, 60),
        'location': 'Endereço ou link de telemedicina',
        'notes': 'Notas sobre o paciente',
    }

    response = client.post('/api/agendamentos', json=data, headers={'Authorization': f'Bearer {token}'})
    response_data = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert response_data['patient_id'] == data['patient_id']
    assert response_data['date_time'] == data['date_time']
    assert response_data['type'] == data['type']
    assert response_data['status'] == data['status']
    assert response_data['estimated_duration'] == data['estimated_duration']
    assert response_data['location'] == data['location']
    assert response_data['notes'] == data['notes']
    assert 'id' in response_data
    assert 'created_at' in response_data
    assert 'updated_at' in response_data


def test_create_appointment_without_authorization(client: TestClient, date_in_future: str) -> None:
    data = {
        'patient_id': '123',
        'professional_id': '456',
        'date_time': date_in_future,
        'type': AppointmentTypes.CONSULTATION,
        'status': AppointmentStatus.SCHEDULED,
        'estimated_duration': random.randint(1, 60),
        'location': 'Endereço ou link de telemedicina',
        'notes': 'Notas sobre o paciente',
    }

    response = client.post('/api/agendamentos', json=data)
    response_data = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response_data['detail'] == 'Not authenticated'


def test_create_appointment_with_invalid_patient_id(
    client: TestClient, healthcare_profissional: UserSchema, token: str, date_in_future: str
) -> None:
    data = {
        'patient_id': 'invalid-uuid-123',
        'professional_id': str(healthcare_profissional.id),
        'date_time': date_in_future,
        'type': AppointmentTypes.CONSULTATION,
        'status': AppointmentStatus.SCHEDULED,
        'estimated_duration': 30,
        'location': 'Sala 205',
        'notes': 'Paciente inexistente',
    }

    response = client.post('/api/agendamentos', json=data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'patient_id' in response.text


def test_create_appointment_with_past_date(
    client: TestClient, patient: UserSchema, healthcare_profissional: UserSchema, token: str
) -> None:
    date_in_past = datetime.now() - timedelta(days=random.randint(1, 30))

    data = {
        'patient_id': str(patient.id),
        'professional_id': str(healthcare_profissional.id),
        'date_time': date_in_past.isoformat(),
        'type': AppointmentTypes.CONSULTATION,
        'status': AppointmentStatus.SCHEDULED,
        'estimated_duration': 30,
        'location': 'Sala 205',
        'notes': 'Data inválida',
    }

    response = client.post('/api/agendamentos', json=data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert 'Não é possível agendar no passado' in response.json()['detail']


def test_create_conflicting_appointment(
    client: TestClient, patient: UserSchema, healthcare_profissional: UserSchema, token: str, date_in_future: str
) -> None:
    base_data = {
        'patient_id': str(patient.id),
        'professional_id': str(healthcare_profissional.id),
        'date_time': date_in_future,
        'type': AppointmentTypes.CONSULTATION,
        'status': AppointmentStatus.SCHEDULED,
        'estimated_duration': 60,
        'location': 'Sala 205',
        'notes': 'Conflito',
    }

    response1 = client.post('/api/agendamentos', json=base_data, headers={'Authorization': f'Bearer {token}'})
    assert response1.status_code == HTTPStatus.CREATED

    response2 = client.post('/api/agendamentos', json=base_data, headers={'Authorization': f'Bearer {token}'})
    assert response2.status_code == HTTPStatus.CONFLICT
    assert 'Já existe um agendamento no mesmo horário' in response2.json()['detail']


def test_create_appointment_with_missing_fields(client: TestClient, token: str) -> None:
    incomplete_data = {'date_time': datetime.now().isoformat(), 'type': AppointmentTypes.CONSULTATION}

    response = client.post('/api/agendamentos', json=incomplete_data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'patient_id' in response.text
    assert 'location' in response.text


def test_patient_creating_appointment_for_another_patient(
    client: TestClient,
    another_patient: UserSchema,
    healthcare_profissional: UserSchema,
    token: str,
    date_in_future: str,
) -> None:
    data = {
        'patient_id': str(another_patient.id),
        'professional_id': str(healthcare_profissional.id),
        'date_time': date_in_future,
        'type': AppointmentTypes.CONSULTATION,
        'status': AppointmentStatus.SCHEDULED,
        'estimated_duration': 30,
        'location': 'Sala 205',
        'notes': 'Acesso não autorizado',
    }

    response = client.post('/api/agendamentos', json=data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert 'Você não tem permissão para acessar este recurso' in response.json()['detail']
