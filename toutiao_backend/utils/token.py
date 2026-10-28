"""
JWT令牌工具
"""
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "news_app_secret_key_2024"
ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 7


def create_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
