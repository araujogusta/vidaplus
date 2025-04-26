from http import HTTPStatus


class ApplicationError(Exception):
    code = HTTPStatus.INTERNAL_SERVER_ERROR


class EmailAlreadyExistsError(ApplicationError):
    code = HTTPStatus.BAD_REQUEST

    def __init__(self) -> None:
        super().__init__('O email já foi cadastrado')


class AuthenticationError(ApplicationError):
    code = HTTPStatus.UNAUTHORIZED

    def __init__(self) -> None:
        super().__init__('Email ou senha inválidos')


class InvalidTokenError(ApplicationError):
    code = HTTPStatus.UNAUTHORIZED

    def __init__(self) -> None:
        super().__init__('Token inválido')


class ExpiredTokenError(ApplicationError):
    code = HTTPStatus.UNAUTHORIZED

    def __init__(self) -> None:
        super().__init__('Token expirado')


class TokenRefreshError(ApplicationError):
    code = HTTPStatus.UNAUTHORIZED

    def __init__(self) -> None:
        super().__init__('Não foi possível atualizar o token')


class PermissionRequiredError(ApplicationError):
    code = HTTPStatus.FORBIDDEN

    def __init__(self) -> None:
        super().__init__('Você não tem permissão para acessar este recurso')


class SchedulingInPastError(ApplicationError):
    code = HTTPStatus.BAD_REQUEST

    def __init__(self) -> None:
        super().__init__('Não é possível agendar no passado')


class SchedulingTimeConflictError(ApplicationError):
    code = HTTPStatus.CONFLICT

    def __init__(self) -> None:
        super().__init__('Já existe um agendamento no mesmo horário')


class PatientNotFoundError(ApplicationError):
    code = HTTPStatus.NOT_FOUND

    def __init__(self) -> None:
        super().__init__('Paciente não encontrado')
