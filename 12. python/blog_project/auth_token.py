from datetime import datetime, timedelta, timezone
import os

import constant
from dotenv import load_dotenv
from jose import jwt, JWTError
from schemas import TokenData

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))

if not SECRET_KEY:
    raise RuntimeError(f"{constant.MSG_MISSING_ENV}: SECRET_KEY")

if not ALGORITHM:
    raise RuntimeError(f"{constant.MSG_MISSING_ENV}: JWT_ALGORITHM")


def create_access_token(data: dict):
    """
        Handles the create access token operation.
        
        Parameters:
        data (dict): The data value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    """
        Handles the verify token operation.
        
        Parameters:
        token (str): The token value used by this function.
        credentials exception (Any): The credentials exception value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise credentials_exception
        token_data = TokenData(username=username, user_id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data
    
