from datetime import timedelta
from typing import Dict, Any
from django.utils import timezone
import jwt

# use a longer default key to avoid insecure length warnings in tests
SECRET_KEY = "replace-with-a-very-long-secret-string-at-least-32-bytes"
ALGORITHM = "HS256"


def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    # use timezone-aware now and convert to UTC timestamp if necessary
    expire = timezone.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
