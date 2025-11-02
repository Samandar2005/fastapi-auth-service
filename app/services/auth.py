from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserOut
from app.utils.security import get_password_hash, verify_password
from fastapi import HTTPException, status
from datetime import datetime
from jose import JWTError, jwt
from app.core.config import settings
import redis.asyncio as redis


async def create_user(db: AsyncSession, user_in: UserCreate) -> UserOut:
    result = await db.execute(select(User).filter(User.email == user_in.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Default rolni topish
    result = await db.execute(select(Role).filter(Role.name == "user"))
    default_role = result.scalars().first()
    if not default_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Default user role not found"
        )

    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=False,
        role_id=default_role.id
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return UserOut.from_orm(new_user)

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def blacklist_token(token: str, redis_client: redis.Redis):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        exp = payload.get("exp")
        jti = payload.get("jti")
        if exp is None:
            return
    except JWTError:
        return

    # Normalize exp to timestamp (int)
    now_ts = int(datetime.utcnow().timestamp())
    if isinstance(exp, (float, int)):
        exp_ts = int(exp)
    else:
        try:
            exp_ts = int(exp)
        except Exception:
            # If exp is unexpected type, skip
            return

    expire_in = exp_ts - now_ts
    if expire_in > 0:
        key = f"blacklist:{jti}" if jti else f"blacklist:{token}"
        await redis_client.setex(key, expire_in, "true")
