from datetime import datetime, timedelta
from uuid import UUID

from vidaplus.main.enums.roles import Roles
from vidaplus.main.exceptions import PermissionRequiredError, SchedulingInPastError, SchedulingTimeConflictError
from vidaplus.main.schemas.appointment import AppointmentSchema, CreateAppointmentSchema
from vidaplus.main.schemas.user import PublicUserSchema
from vidaplus.models.repositories.interfaces.appointment_repository_interface import AppointmentRepositoryInterface


class AppointmentService:
    def __init__(self, repository: AppointmentRepositoryInterface) -> None:
        self.repository = repository

    def create(self, appointment: CreateAppointmentSchema, creator: PublicUserSchema) -> AppointmentSchema:
        if appointment.patient_id != creator.id and creator.role == Roles.PATIENT:
            raise PermissionRequiredError()

        if not appointment.date_time > datetime.now():
            raise SchedulingInPastError()
        
        if self.has_time_conflict(appointment.professional_id, appointment.date_time, appointment.estimated_duration):
            raise SchedulingTimeConflictError()

        return self.repository.create(appointment)

    def has_time_conflict(self, professional_id: UUID, appointment_start: datetime, duration: int) -> bool:
        appointment_end = appointment_start + timedelta(minutes=duration)
        existing_appointments = self.repository.get_by_professional_id(professional_id)

        for existing_appointment in existing_appointments:
            existing_appointment_start = existing_appointment.date_time
            existing_appointment_end = existing_appointment_start + timedelta(minutes=existing_appointment.estimated_duration)

            if (appointment_start <= existing_appointment_start) and (appointment_end >= existing_appointment_end):
                return True
            
        return False