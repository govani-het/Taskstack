"""Access control helpers."""

from functools import wraps
from inspect import signature

from fastapi import HTTPException, Request, status

from app.authentication.role_base_auth_token import verify_token


def _get_current_user(func, args, kwargs) -> dict:
    """Resolve the current user from endpoint arguments.
    
    Args:
        func: Wrapped function.
        args: Positional arguments passed to the wrapped function.
        kwargs: Keyword arguments passed to the wrapped function.
    
    Returns:
        dict: User or token payload.
    
    Raises:
        HTTPException: If authentication or authorization fails.
    """
    bound_arguments = signature(func).bind_partial(*args, **kwargs)
    current_user = bound_arguments.arguments.get("current_user")
    if current_user is not None:
        return current_user

    request = bound_arguments.arguments.get("request")
    if not isinstance(request, Request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.split(" ", 1)[1]
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)


def require_roles(allowed_roles: list[str]):
    """Create a decorator that restricts access to allowed roles.
    
    Args:
        allowed_roles: Roles allowed to access the wrapped endpoint.
    
    Raises:
        HTTPException: If authentication or authorization fails.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = _get_current_user(func, args, kwargs)

            if current_user.get("role") not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You Don't have permission to access this resource",
                )

            kwargs["current_user"] = current_user
            return await func(*args, **kwargs)

        return wrapper

    return decorator
