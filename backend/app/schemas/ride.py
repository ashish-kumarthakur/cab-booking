from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.ride import RideStatus


class RideCreate(BaseModel):
    pickup_lat: float = Field(..., ge=-90, le=90)
    pickup_lng: float = Field(..., ge=-180, le=180)
    drop_lat: float = Field(..., ge=-90, le=90)
    drop_lng: float = Field(..., ge=-180, le=180)
    pickup_address: str
    drop_address: str


class RideEstimate(BaseModel):
    distance_meters: float
    duration_secs: int
    fare_estimate: float
    currency: str = "USD"


class RideStatusUpdate(BaseModel):
    status: RideStatus


class RideResponse(BaseModel):
    id: UUID
    rider_id: UUID
    driver_id: Optional[UUID]
    pickup_address: str
    drop_address: str
    status: RideStatus
    fare_estimate: Optional[float]
    fare_actual: Optional[float]
    distance_meters: Optional[float]
    duration_secs: Optional[int]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


