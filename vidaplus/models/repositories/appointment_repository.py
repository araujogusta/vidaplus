from uuid import UUID

from sqlalchemy import select
from vidaplus.main.schemas.appointment import AppointmentSchema, CreateAppointmentSchema
from vidaplus.models.config.connection import DatabaseConnectionHandler
from vidaplus.models.entities.appointment import Appointment
from vidaplus.models.repositories.interfaces.appointment_repository_interface import AppointmentRepositoryInterface


class AppointmentRepository(AppointmentRepositoryInterface):
    def create(self, new_appointment: CreateAppointmentSchema) -> AppointmentSchema:
        with DatabaseConnectionHandler() as db:
            try:
                appointment = Appointment(**new_appointment.model_dump())
                db.session.add(appointment)
                db.session.commit()
                db.session.refresh(appointment)
                return AppointmentSchema.model_validate(appointment)
            except Exception as e:
                db.session.rollback()
                raise e
    
    def get_by_professional_id(self, professional_id: UUID) -> list[AppointmentSchema]:
        with DatabaseConnectionHandler() as db:
            try:
                appointments = db.session.scalars(
                    select(Appointment).where(Appointment.professional_id == professional_id)
                )

                return [AppointmentSchema.model_validate(appointment) for appointment in appointments]
            except Exception as e:
                db.session.rollback()
                raise e
