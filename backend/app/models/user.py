from sqlalchemy import Column, String, Float, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from app.core.database import Base


class UserRole(str, enum.Enum):
    RIDER = "rider"
    DRIVER = "driver"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clerk_user_id = Column(String(255), unique=True, nullable=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), unique=True, nullable=True, index=True)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.RIDER)
    profile_pic = Column(String(500), nullable=True)
    rating_avg = Column(Float, default=0.0)
    wallet_balance = Column(Float, default=0.0)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
