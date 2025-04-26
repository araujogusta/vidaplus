from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter

from vidaplus.main.enums.roles import Roles
from vidaplus.main.schemas.user import PublicUserSchema, RequestCreateUserSchema
from vidaplus.models.repositories.user_repository import UserRepository
from vidaplus.services.user_service import UserService

router = APIRouter(prefix='/api/pacientes', tags=['Pacientes'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=PublicUserSchema)
def register_patient(data: RequestCreateUserSchema) -> PublicUserSchema:
    user_repository = UserRepository()
    user_service = UserService(user_repository)
    return user_service.new_patient(data)


@router.get('/', status_code=HTTPStatus.OK, response_model=list[PublicUserSchema])
def list_patients() -> list[PublicUserSchema]:
    user_repository = UserRepository()
    user_service = UserService(user_repository)
    return user_service.all(Roles.PATIENT)


@router.get('/{patient_id}', status_code=HTTPStatus.OK, response_model=PublicUserSchema)
def get_patient(patient_id: UUID) -> PublicUserSchema:
    user_repository = UserRepository()
    user_service = UserService(user_repository)
    return user_service.get_by_id(patient_id)
