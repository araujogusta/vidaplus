from enum import Enum


class Roles(str, Enum):
    ADMIN = 'ADMIN'
    PATIENT = 'PATIENT'
