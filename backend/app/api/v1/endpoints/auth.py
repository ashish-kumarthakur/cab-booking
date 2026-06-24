from fastapi import APIRouter, Depends
from app.core.security import verify_token

router = APIRouter()


@router.post("/session")
async def verify_session(auth_data: dict = Depends(verify_token)):
    return {
        "user_id": auth_data["user_id"],
        "email": auth_data.get("email"),
        "role": auth_data.get("role"),
        "authenticated": True,
    }
