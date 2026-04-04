"""
    Defines the main module.
    
    Parameters:
    None (None): This module does not accept parameters.
    
    Returns:
    None: This module does not return a value.
"""

from pathlib import Path

from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles
import models
from database import engine
from passlib.context import CryptContext
from router import blog, user, login, comments, reply, user_profile


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(engine)


app = FastAPI()

uploads_dir = Path(__file__).resolve().parent / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(comments.router)
app.include_router(reply.router)
app.include_router(user_profile.router)



@app.get("/", status_code=status.HTTP_200_OK)
def index():
    """
        Handles the index operation.
        
        Parameters:
        None (None): This function does not require parameters.
        
        Returns:
        Any: The result produced by this function.
    """
    return {"message": "Hello World"}
