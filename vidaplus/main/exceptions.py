class ApplicationError(Exception):
    code = 500


class EmailAlreadyExistsError(ApplicationError):
    code = 400

    def __init__(self) -> None:
        super().__init__('O email já foi cadastrado')
