from abc import ABC, abstractmethod
from uuid import UUID

from vidaplus.main.schemas.appointment import AppointmentSchema, CreateAppointmentSchema


class AppointmentRepositoryInterface(ABC):
    @abstractmethod
    def create(self, new_appointment: CreateAppointmentSchema) -> AppointmentSchema:
        pass

    @abstractmethod
    def get_by_professional_id(self, professional_id: UUID) -> list[AppointmentSchema]:
        pass