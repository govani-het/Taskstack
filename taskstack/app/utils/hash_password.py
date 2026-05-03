"""Password hashing helpers."""


import bcrypt

def hash_password(password: str) -> str:
    """Hash a plain-text password.
    
    Args:
        password: Password.
    
    Returns:
        str: Result of the operation.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
