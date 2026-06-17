from fastapi import Depends, HTTPException, status
from authx import RequestToken
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from utils.security import security
from settings.db import get_db
from models.user import User

async def get_current_user(
    token: RequestToken = Depends(security.access_token_required),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        user_id = int(token.sub)
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user identifier in token",
        ) from exc

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )
    return user

async def get_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Admin role required.",
        )
    return current_user
