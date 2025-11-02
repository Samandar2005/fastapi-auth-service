from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Parolni hash qilish uchun
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
# Token yaratish funksiyalari `app.utils.jwt` modulida saqlangan.
# Bu yerda ularni import qilib qayta eksport qilamiz, shunda boshqa modul-larda
# `app.utils.security.create_access_token` chaqirilsa ham ishlaydi.
from app.utils.jwt import create_access_token, create_refresh_token

