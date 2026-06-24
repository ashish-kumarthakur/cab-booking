from typing import Optional, Dict
import httpx
from jose import jwt, jwk, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

security = HTTPBearer()

_jwks_cache: Optional[Dict] = None


async def _get_clerk_jwks() -> Dict:
    global _jwks_cache
    if _jwks_cache is not None:
        return _jwks_cache

    if not settings.CLERK_ISSUER:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="CLERK_ISSUER is not configured",
        )

    issuer = settings.CLERK_ISSUER.rstrip("/")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{issuer}/.well-known/jwks.json", timeout=10.0)
        response.raise_for_status()
        _jwks_cache = response.json()
        return _jwks_cache


async def _verify_clerk_token(token: str) -> dict:
    jwks = await _get_clerk_jwks()
    issuer = settings.CLERK_ISSUER.rstrip("/")

    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    rsa_key = None
    for key in jwks.get("keys", []):
        if key.get("kid") == unverified_header.get("kid"):
            rsa_key = jwk.construct(key)
            break

    if not rsa_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            issuer=issuer,
            options={"verify_aud": False},
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials

    try:
        if settings.CLERK_SECRET_KEY and settings.CLERK_ISSUER:
            payload = await _verify_clerk_token(token)
        elif settings.SUPABASE_KEY:
            payload = jwt.decode(
                token,
                settings.SUPABASE_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        else:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )

        user_id: Optional[str] = payload.get("sub") or payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

        return {
            "user_id": user_id,
            "email": payload.get("email"),
            "name": payload.get("name") or payload.get("full_name"),
            "role": payload.get("role"),
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


def get_current_user_id(auth_data: dict = Depends(verify_token)) -> str:
    return auth_data["user_id"]


async def get_current_user(
    auth_data: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
) -> User:
    clerk_id = auth_data["user_id"]

    result = await db.execute(select(User).where(User.clerk_user_id == clerk_id))
    user = result.scalar_one_or_none()

    if not user:
        email = auth_data.get("email") or f"{clerk_id}@users.clerk"
        name = auth_data.get("name") or "User"
        user = User(
            clerk_user_id=clerk_id,
            name=name,
            email=email,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user
