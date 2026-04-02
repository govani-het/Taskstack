from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from schemas import TokenData


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


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
    
