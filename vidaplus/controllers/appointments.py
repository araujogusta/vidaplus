from http import HTTPStatus

from fastapi import APIRouter, Depends

from vidaplus.main.schemas.appointment import AppointmentSchema, CreateAppointmentSchema
from vidaplus.main.schemas.user import PublicUserSchema
from vidaplus.models.repositories.appointment_repository import AppointmentRepository
from vidaplus.services.appointment_service import AppointmentService
from vidaplus.services.auth_service import AuthService

router = APIRouter(prefix='/api/agendamentos', tags=['Agendamentos'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AppointmentSchema)
def create_appointment(
    data: CreateAppointmentSchema, creator: PublicUserSchema = Depends(AuthService.get_current_user)
) -> AppointmentSchema:
    repository = AppointmentRepository()
    service = AppointmentService(repository)
    return service.create(data, creator)
