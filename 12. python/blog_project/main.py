"""
    Defines the main module.
    
    Parameters:
    None (None): This module does not accept parameters.
    
    Returns:
    None: This module does not return a value.
"""

from fastapi import FastAPI, status
import models
from database import engine
from passlib.context import CryptContext
from router import blog, user, login, comments, reply, user_profile


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(engine)


app = FastAPI()

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
