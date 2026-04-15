from typing import Generic, TypeVar, Optional
from pydantic import BaseModel


DataT = TypeVar('DataT')

class APIResponse(BaseModel, Generic[DataT]):
    success: Optional[bool] = None
    error: Optional[bool] = None
    message: str
    data: Optional[DataT] = None

    @classmethod
    def success_response(cls, message: str, data: Optional[DataT] = None) -> "APIResponse[DataT]":
        """Generates a standardized success response."""
        return cls(
            success=True,
            error=None,
            message=message,
            data=data
        )

    @classmethod
    def error_response(cls, message: str) -> "APIResponse[DataT]":
        """Generates a standardized error response."""
        return cls(
            success=None,
            error=True,
            message=message,
            data=None
        )