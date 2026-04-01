"""Application entrypoint that mounts routers and exposes base endpoints."""

from fastapi import FastAPI, status
import models
from database import engine
from passlib.context import CryptContext
from router import blog, user, login, comments, reply





pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(engine)


app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(comments.router)
app.include_router(reply.router)





@app.get("/", status_code=status.HTTP_200_OK)
def index():
    """Health-check style root endpoint."""
    return {"message": "Hello World"}
