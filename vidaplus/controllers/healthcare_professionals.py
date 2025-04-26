from http import HTTPStatus

from fastapi import APIRouter, Depends

from vidaplus.main.schemas.user import PublicUserSchema, RequestCreateUserSchema
from vidaplus.models.repositories.user_repository import UserRepository
from vidaplus.services.auth_service import AuthService
from vidaplus.services.user_service import UserService

router = APIRouter(prefix='/api/profissionais', tags=['Profissionais de Saúde'])


@router.post('/', status_code=HTTPStatus.CREATED)
def create_healthcare_professional(
    data: RequestCreateUserSchema, creator: PublicUserSchema = Depends(AuthService.get_current_user)
) -> PublicUserSchema:
    repository = UserRepository()
    service = UserService(repository)
    return service.new_healthcare_professional(data, creator)
