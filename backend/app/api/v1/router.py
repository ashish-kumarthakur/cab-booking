from fastapi import APIRouter
from app.api.v1.endpoints import auth, rides, payments, reviews, users, websocket, drivers

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(drivers.router, prefix="/drivers", tags=["drivers"])
api_router.include_router(rides.router, prefix="/rides", tags=["rides"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(websocket.router, tags=["websocket"])

