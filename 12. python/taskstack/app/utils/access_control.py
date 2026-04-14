from fastapi import HTTPException, status
from typing import Iterable


def check_allowed_roles(current_user: dict, allowed_roles: Iterable[str], action: str = "access this resource") -> None:
    """Raise HTTP 403 if current_user role is not in allowed_roles."""
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    user_role = current_user.get("role")
    if user_role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"User with role '{user_role}' is not authorized to {action}. "
                f"Allowed roles: {', '.join(allowed_roles)}"
            ),
        )
