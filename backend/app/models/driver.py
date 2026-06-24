from sqlalchemy import Column, String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from geoalchemy2 import Geometry
from app.core.database import Base


class DriverStatus(str, enum.Enum):
    ACTIVE = "active"
    OFFLINE = "offline"
    ON_RIDE = "on_ride"


class Driver(Base):
    __tablename__ = "drivers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    vehicle_info = Column(String(500), nullable=True)  # JSON string or separate fields
    vehicle_number = Column(String(50), nullable=True)
    license_number = Column(String(100), nullable=True)
    verified = Column(Boolean, default=False)
    current_location = Column(Geometry("POINT", srid=4326), nullable=True)  # PostGIS Point
    status = Column(SQLEnum(DriverStatus), default=DriverStatus.OFFLINE)
    
    # Relationship
    user = relationship("User", backref="driver_profile")
    
    def __repr__(self):
        return f"<Driver(id={self.id}, user_id={self.user_id}, status={self.status})>"


