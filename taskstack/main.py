"""Application entry point."""


from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.routes.login import router as auth_router
from app.api.v1 import router as v1_router
from app.schemas.response_schemas import APIResponse

app = FastAPI(title="TaskStack API")

# Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Convert request validation errors into the standard API format.
    """
    errors = [
        {
            "loc": list(error.get("loc", [])),
            "msg": error.get("msg", ""),
            "type": error.get("type", ""),
        }
        for error in exc.errors()
    ]

    response = APIResponse.error_response(
        error="Validation failed"
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response.model_dump()
    )


@app.exception_handler(StarletteHTTPException)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Convert HTTP exceptions into the standard API format.
    Catch both Starlette and FastAPI HTTPExceptions.
    """
    response = APIResponse.error_response(
        error=exc.detail
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump()
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Convert unhandled exceptions into the standard API format.
    """
    # In a production environment, you might want to log the exception here
    response = APIResponse.error_response(
        error=str(exc) if app.debug else "An unexpected error occurred"
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump()
    )


app.include_router(auth_router)
app.include_router(v1_router)

@app.get("/", status_code=status.HTTP_200_OK)
def index():
    """Return the application status message."""
    return APIResponse.success_response(
        message="TaskStack API running",
        data={"status": "active"}
    )
