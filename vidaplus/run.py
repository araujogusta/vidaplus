from fastapi import FastAPI, HTTPException, Request

from vidaplus.controllers import patients
from vidaplus.main.exceptions import ApplicationError

app = FastAPI(title='SSGHSS VidaPlus')
app.include_router(patients.router)


@app.exception_handler(ApplicationError)
def application_error_handler(request: Request, exc: ApplicationError) -> None:
    raise HTTPException(status_code=exc.code, detail=str(exc))
