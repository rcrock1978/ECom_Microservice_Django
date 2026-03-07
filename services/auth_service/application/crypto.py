import hashlib
import os
from typing import Tuple


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
    return salt.hex() + dk.hex()


def verify_password(password: str, hashed: str) -> bool:
    salt = bytes.fromhex(hashed[:32])
    stored = hashed[32:]
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
    return dk.hex() == stored
