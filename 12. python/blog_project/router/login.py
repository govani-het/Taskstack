from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
import constant
import schemas
from sqlalchemy.orm import Session
from database import get_db
import models
from passlib.context import CryptContext
from auth_token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from repository import password_reset as password_reset_repository




pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

router = APIRouter(tags=["login"])

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
        Handles the login operation.
        
        Parameters:
        request (OAuth2PasswordRequestForm): The request value used by this function.
        db (Session): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    user = db.query(models.User).filter(models.User.email == request.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constant.MSG_INVALID_CREDENTIALS,
        )
    
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constant.MSG_INVALID_PASSWORD,
        )
    
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id}
    )
    
    return {
        constant.RESP_KEY_ACCESS_TOKEN: access_token,
        constant.RESP_KEY_TOKEN_TYPE: constant.TOKEN_TYPE_BEARER,
    }


@router.post("/forgot-password/token", status_code=status.HTTP_200_OK)
def forgot_password_token(
    request: schemas.ForgotPasswordTokenRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
        Handles the forgot password token operation.
        
        Parameters:
        request (schemas ForgotPasswordTokenRequest): The request value used by this function.
        background tasks (BackgroundTasks): The background tasks value used by this function.
        db (Session): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    return password_reset_repository.create_reset_token(
        request=request,
        db=db,
        background_tasks=background_tasks,
    )


@router.post("/forgot-password/reset", status_code=status.HTTP_200_OK)
def forgot_password_reset(
    request: schemas.ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    """
        Handles the forgot password reset operation.
        
        Parameters:
        request (schemas ResetPasswordRequest): The request value used by this function.
        db (Session): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    return password_reset_repository.reset_password(request=request, db=db)
