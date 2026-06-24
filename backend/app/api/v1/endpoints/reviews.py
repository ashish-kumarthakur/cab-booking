from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.review import Review
from app.models.ride import Ride, RideStatus
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse

router = APIRouter()


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_data: ReviewCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Ride).where(
            Ride.id == review_data.ride_id,
            (Ride.rider_id == user.id) | (Ride.driver_id == user.id)
        )
    )
    ride = result.scalar_one_or_none()
    
    if not ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ride not found",
        )
    
    if ride.status != RideStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only review completed rides",
        )
    
    if ride.rider_id == user.id:
        if review_data.rated_id != str(ride.driver_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only rate the driver for this ride",
            )
    elif ride.driver_id == user.id:
        if review_data.rated_id != str(ride.rider_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only rate the rider for this ride",
            )
    
    existing = await db.execute(
        select(Review).where(
            Review.ride_id == review_data.ride_id,
            Review.rater_id == user.id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Review already exists for this ride",
        )
    
    review = Review(
        ride_id=review_data.ride_id,
        rater_id=user.id,
        rated_id=UUID(review_data.rated_id),
        rating=review_data.rating,
        comment=review_data.comment,
    )
    
    db.add(review)
    await db.commit()
    await db.refresh(review)
    
    return review


@router.get("/ride/{ride_id}", response_model=List[ReviewResponse])
async def get_ride_reviews(
    ride_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Review).where(Review.ride_id == ride_id)
    )
    reviews = result.scalars().all()
    
    return reviews


@router.get("/user/{user_id}", response_model=List[ReviewResponse])
async def get_user_reviews(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Review).where(Review.rated_id == user_id)
        .order_by(Review.created_at.desc())
    )
    reviews = result.scalars().all()
    
    return reviews
