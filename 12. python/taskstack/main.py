"""Application entry point."""


from fastapi import FastAPI
from starlette import status

from app.api.v1.routes.login import router as auth_router
from app.api.v1 import router as v1_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(v1_router)

@app.get("/", status_code=status.HTTP_200_OK)
def index():
    """Return the application status message."""
    return {"message": "Hello World"}
