from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserOut
from app.db.session import get_db
from app.db.redis import get_redis
from typing import List
import redis.asyncio as redis

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis)
) -> UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Avval tokenni parsiq qilib, jti va sub ni o'qiymiz, keyin blacklist tekshiramiz
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        jti: str | None = payload.get("jti")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Blacklist'da jti borligini tekshirish (agar jti bo'lsa), aks holda token string bo'yicha tekshirish
    if jti:
        if await redis_client.get(f"blacklist:{jti}"):
            raise credentials_exception
    else:
        if await redis_client.get(f"blacklist:{token}"):
            raise credentials_exception

    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return UserOut.from_orm(user)

def require_permissions(required_permissions: List[str]):
    async def check_permissions(
        current_user: UserOut = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ) -> UserOut:
        # Superadmin bo'lsa, barcha ruxsatlarga ega
        if current_user.is_superuser:
            return current_user

        # Foydalanuvchi rolini olish
        if not current_user.role_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no role assigned"
            )

        result = await db.execute(select(Role).filter(Role.id == current_user.role_id))
        role = result.scalars().first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Role not found"
            )

        # Ruxsatlarni tekshirish
        role_permissions = role.permissions.split(",") if role.permissions else []
        if not all(perm in role_permissions for perm in required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        return current_user
    return check_permissions