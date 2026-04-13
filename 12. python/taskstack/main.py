
from fastapi import FastAPI
from starlette import status

from app.authentication.login import router as auth_router

app = FastAPI()
app.include_router(auth_router)

@app.get("/", status_code=status.HTTP_200_OK)
def index():
    return {"message": "Hello World"}

