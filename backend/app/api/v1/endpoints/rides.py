from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from uuid import UUID
from datetime import datetime
from geoalchemy2 import WKTElement

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.ride import Ride, RideStatus
from app.models.user import User
from app.models.driver import Driver, DriverStatus
from app.schemas.ride import RideCreate, RideResponse, RideEstimate, RideStatusUpdate
from app.services.maps import calculate_distance_and_duration

router = APIRouter()


@router.get("/estimate", response_model=RideEstimate)
async def estimate_ride(
    pickup_lat: float = Query(..., ge=-90, le=90),
    pickup_lng: float = Query(..., ge=-180, le=180),
    drop_lat: float = Query(..., ge=-90, le=90),
    drop_lng: float = Query(..., ge=-180, le=180),
):
    origin = (pickup_lat, pickup_lng)
    destination = (drop_lat, drop_lng)
    result = calculate_distance_and_duration(origin, destination)
    
    return RideEstimate(
        distance_meters=result["distance_meters"],
        duration_secs=result["duration_secs"],
        fare_estimate=result["fare_estimate"],
    )


@router.post("/request", response_model=RideResponse, status_code=status.HTTP_201_CREATED)
async def create_ride_request(
    ride_data: RideCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    origin = (ride_data.pickup_lat, ride_data.pickup_lng)
    destination = (ride_data.drop_lat, ride_data.drop_lng)
    estimate = calculate_distance_and_duration(origin, destination)
    
    pickup_point = WKTElement(f"POINT({ride_data.pickup_lng} {ride_data.pickup_lat})", srid=4326)
    drop_point = WKTElement(f"POINT({ride_data.drop_lng} {ride_data.drop_lat})", srid=4326)
    
    ride = Ride(
        rider_id=user.id,
        pickup_point=pickup_point,
        drop_point=drop_point,
        pickup_address=ride_data.pickup_address,
        drop_address=ride_data.drop_address,
        fare_estimate=estimate["fare_estimate"],
        distance_meters=estimate["distance_meters"],
        duration_secs=estimate["duration_secs"],
        status=RideStatus.PENDING,
    )
    
    db.add(ride)
    await db.commit()
    await db.refresh(ride)
    
    return ride


@router.get("/{ride_id}", response_model=RideResponse)
async def get_ride(
    ride_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Ride).where(
            Ride.id == ride_id,
            (Ride.rider_id == user.id) | (Ride.driver_id == user.id)
        )
    )
    ride = result.scalar_one_or_none()
    
    if not ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ride not found",
        )
    
    return ride


@router.get("/", response_model=List[RideResponse])
async def get_ride_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Ride)
        .where((Ride.rider_id == user.id) | (Ride.driver_id == user.id))
        .order_by(Ride.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    rides = result.scalars().all()
    
    return rides


@router.put("/{ride_id}/status", response_model=RideResponse)
async def update_ride_status(
    ride_id: UUID,
    status_update: RideStatusUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Ride).where(
            Ride.id == ride_id,
            (Ride.rider_id == user.id) | (Ride.driver_id == user.id)
        )
    )
    ride = result.scalar_one_or_none()
    
    if not ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ride not found",
        )
    
    ride.status = status_update.status
    
    if status_update.status == RideStatus.IN_PROGRESS and not ride.started_at:
        ride.started_at = datetime.utcnow()
    elif status_update.status == RideStatus.COMPLETED and not ride.completed_at:
        ride.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(ride)
    
    return ride


@router.get("/nearby/drivers")
async def get_nearby_drivers(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(5.0, ge=0.1, le=50.0),
    db: AsyncSession = Depends(get_db),
):
    search_point = WKTElement(f"POINT({lng} {lat})", srid=4326)
    
    result = await db.execute(
        select(Driver, User)
        .join(User, Driver.user_id == User.id)
        .where(
            Driver.status == DriverStatus.ACTIVE,
            Driver.verified == True,
            Driver.current_location.isnot(None),
            func.ST_DWithin(
                Driver.current_location,
                search_point,
                radius_km * 1000
            )
        )
        .limit(10)
    )
    
    drivers = result.all()
    
    return [
        {
            "driver_id": str(driver.id),
            "user_id": str(driver.user_id),
            "name": user.name,
            "rating": user.rating_avg,
            "vehicle_info": driver.vehicle_info,
            "distance_km": None,
        }
        for driver, user in drivers
    ]
