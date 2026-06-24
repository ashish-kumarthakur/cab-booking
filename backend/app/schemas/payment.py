from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.payment import PaymentStatus


class PaymentCreate(BaseModel):
    ride_id: UUID
    amount: float


class PaymentResponse(BaseModel):
    id: UUID
    ride_id: UUID
    stripe_payment_intent_id: Optional[str]
    amount: float
    currency: str
    status: PaymentStatus
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


