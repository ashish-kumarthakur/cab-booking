from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.core.database import Base


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ride_id = Column(UUID(as_uuid=True), ForeignKey("rides.id"), nullable=False, index=True)
    rater_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # Who is rating
    rated_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # Who is being rated
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ride = relationship("Ride", back_populates="reviews")
    rater = relationship("User", foreign_keys=[rater_id], backref="reviews_given")
    rated = relationship("User", foreign_keys=[rated_id], backref="reviews_received")
    
    def __repr__(self):
        return f"<Review(id={self.id}, ride_id={self.ride_id}, rating={self.rating})>"


