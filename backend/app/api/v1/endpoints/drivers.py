from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from geoalchemy2 import WKTElement

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.driver import Driver, DriverStatus
from app.models.user import User

router = APIRouter()


@router.post("/register")
async def register_as_driver(
    vehicle_info: str,
    vehicle_number: str,
    license_number: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Driver).where(Driver.user_id == user.id)
    )
    existing_driver = result.scalar_one_or_none()
    
    if existing_driver:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already registered as a driver",
        )
    
    driver = Driver(
        user_id=user.id,
        vehicle_info=vehicle_info,
        vehicle_number=vehicle_number,
        license_number=license_number,
        verified=False,
        status=DriverStatus.OFFLINE,
    )
    
    db.add(driver)
    await db.commit()
    await db.refresh(driver)
    
    return {"message": "Driver registration successful", "driver_id": str(driver.id)}


@router.put("/status")
async def update_driver_status(
    status: DriverStatus,
    lat: float = None,
    lng: float = None,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Driver).where(Driver.user_id == user.id)
    )
    driver = result.scalar_one_or_none()
    
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver profile not found",
        )
    
    driver.status = status
    
    if lat is not None and lng is not None:
        driver.current_location = WKTElement(f"POINT({lng} {lat})", srid=4326)
    
    await db.commit()
    await db.refresh(driver)
    
    return {"message": "Status updated", "status": driver.status.value}
