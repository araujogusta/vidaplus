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


class AdminRoleRequiredError(ApplicationError):
    code = HTTPStatus.FORBIDDEN

    def __init__(self) -> None:
        super().__init__('Você não tem permissão para acessar este recurso')
