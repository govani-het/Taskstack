from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class SubscriptionBase(BaseModel):
    plan_name: str = Field(..., min_length=1, max_length=100)
    validity: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    plan_name: Optional[str] = Field(None, min_length=1, max_length=100)
    validity: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Optional[float] = Field(None, gt=0)


class SubscriptionResponse(SubscriptionBase):
    id: UUID

    class Config:
        from_attributes = True