"""Authentication token utilities."""

from datetime import datetime, timedelta, timezone
import os
from typing import Annotated

from jose import jwt, JWTError
from fastapi import HTTPException, status
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def create_token(
    data: dict,
    token_type: str = "access",
    expires_delta: timedelta | None = None
):
    """Create a signed JWT token.
    
    Args:
        data: Claims to encode in the token.
        token_type: Type of token to create.
        expires_delta: Custom token lifetime.
    
    Raises:
        ValueError: If the provided values are invalid.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    elif token_type == "access":
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    elif token_type == "refresh":
        expire = datetime.now(timezone.utc) + timedelta(
            days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
        )

    else:
        raise ValueError("Invalid token_type")

    to_encode.update({
        "exp": expire,
        "type": token_type
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Get the current user from the bearer token.
    
    Args:
        token: JWT token string.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)



def verify_token(token: str, credentials_exception):
    """Decode and validate a JWT token.
    
    Args:
        token: JWT token string.
        credentials_exception: Exception to raise when token validation fails.
    
    Raises:
        credentials_exception: If the operation fails.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id = payload.get("id")
        role = payload.get("role")
        organization_id = payload.get("organization_id")

        if email is None:
            raise credentials_exception
        return {"email": email, "id": user_id, "role": role, "organization_id": organization_id}
    except JWTError:
        raise credentials_exception


