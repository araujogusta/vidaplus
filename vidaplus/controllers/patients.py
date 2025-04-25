from http import HTTPStatus

from fastapi import APIRouter

from vidaplus.main.schemas.user import PublicUserSchema, RequestCreateUserSchema
from vidaplus.models.repositories.user_repository import UserRepository
from vidaplus.services.user_service import UserService

router = APIRouter(prefix='/api/pacientes', tags=['Pacientes'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=PublicUserSchema)
def register_patient(data: RequestCreateUserSchema) -> PublicUserSchema:
    user_repository = UserRepository()
    user_service = UserService(user_repository)
    return user_service.new_patient(data)
