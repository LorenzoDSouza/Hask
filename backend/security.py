from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, bcrypt_context


def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(password, hashed_password)


def create_access_token(user_id, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    expire_date = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    # JWT claims must be JSON-serializable: `exp` is a Unix timestamp (int) and
    # `sub` must be a string per the JWT spec.
    claims = {"sub": str(user_id), "exp": int(expire_date.timestamp())}
    return jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> int | None:
    """Valida o JWT e retorna o user_id (sub) como int, ou None se invalido."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except (JWTError, ValueError):
        return None
