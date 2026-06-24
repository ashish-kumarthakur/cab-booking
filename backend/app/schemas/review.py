from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class ReviewCreate(BaseModel):
    ride_id: UUID
    rated_id: UUID  # The user being rated (driver or rider)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: UUID
    ride_id: UUID
    rater_id: UUID
    rated_id: UUID
    rating: int
    comment: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


