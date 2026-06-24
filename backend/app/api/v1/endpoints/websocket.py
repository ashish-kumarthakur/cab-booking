from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List
import json
try:
    import redis.asyncio as aioredis
except ImportError:
    import aioredis
from app.core.config import settings

router = APIRouter()

# Store active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.redis_client = None
    
    async def connect_redis(self):
        """Connect to Redis for pub/sub"""
        if not self.redis_client:
            self.redis_client = await aioredis.from_url(settings.REDIS_URL)
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
    
    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except:
                    pass
    
    async def broadcast_to_user(self, user_id: str, message: dict):
        await self.send_personal_message(message, user_id)


manager = ConnectionManager()


@router.websocket("/ws/rider/{rider_id}")
async def websocket_rider(websocket: WebSocket, rider_id: str):
    """WebSocket endpoint for riders to receive ride updates"""
    await manager.connect(websocket, rider_id)
    await manager.connect_redis()
    
    try:
        while True:
            # Listen for messages from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, rider_id)


@router.websocket("/ws/driver/{driver_id}")
async def websocket_driver(websocket: WebSocket, driver_id: str):
    """WebSocket endpoint for drivers to receive ride requests and send location updates"""
    await manager.connect(websocket, driver_id)
    await manager.connect_redis()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle driver location updates
            if message.get("type") == "location_update":
                # Update driver location in database (would be done via API)
                # Broadcast to relevant riders if needed
                pass
            
            # Handle ride acceptance/decline
            if message.get("type") == "accept_ride":
                ride_id = message.get("ride_id")
                # Process ride acceptance
                await manager.broadcast_to_user(
                    message.get("rider_id"),
                    {"type": "ride_accepted", "ride_id": ride_id, "driver_id": driver_id}
                )
            
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, driver_id)


# Helper function to send ride request to driver
async def send_ride_request_to_driver(driver_id: str, ride_data: dict):
    """Send ride request to a specific driver via WebSocket"""
    await manager.broadcast_to_user(
        driver_id,
        {"type": "ride_request", "data": ride_data}
    )


# Helper function to send ride update to rider
async def send_ride_update_to_rider(rider_id: str, update_data: dict):
    """Send ride status update to rider via WebSocket"""
    await manager.broadcast_to_user(
        rider_id,
        {"type": "ride_update", "data": update_data}
    )

