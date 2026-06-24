from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import uuid
import enum
from datetime import datetime
from app.core.database import Base


class RideStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DRIVER_ARRIVED = "driver_arrived"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Ride(Base):
    __tablename__ = "rides"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rider_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    driver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    
    # PostGIS geometry points
    pickup_point = Column(Geometry("POINT", srid=4326), nullable=False)
    drop_point = Column(Geometry("POINT", srid=4326), nullable=False)
    
    # Address strings for display
    pickup_address = Column(String(500), nullable=False)
    drop_address = Column(String(500), nullable=False)
    
    status = Column(SQLEnum(RideStatus), default=RideStatus.PENDING, index=True)
    fare_estimate = Column(Float, nullable=True)  # Estimated fare
    fare_actual = Column(Float, nullable=True)  # Actual fare charged
    distance_meters = Column(Float, nullable=True)
    duration_secs = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    rider = relationship("User", foreign_keys=[rider_id], backref="rides_as_rider")
    driver = relationship("User", foreign_keys=[driver_id], backref="rides_as_driver")
    payments = relationship("Payment", back_populates="ride")
    reviews = relationship("Review", back_populates="ride")
    
    def __repr__(self):
        return f"<Ride(id={self.id}, rider_id={self.rider_id}, status={self.status})>"


