from datetime import datetime, timedelta
from typing import Dict, Any
import jwt

SECRET_KEY = "replace-me"
ALGORITHM = "HS256"


def verify_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
