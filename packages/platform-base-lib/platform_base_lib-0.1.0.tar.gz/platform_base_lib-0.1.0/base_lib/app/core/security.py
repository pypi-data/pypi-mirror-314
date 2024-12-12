from sqlalchemy.ext.asyncio import AsyncSession
from base_lib.interactor.schema.schemas import TokenData
from base_lib.configs.config import settings
import bcrypt
import jwt
from typing import Optional

# Configuration values
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


async def verify_token(token: str, db: AsyncSession) -> Optional[TokenData]:
    """
    Verify a JWT token and return TokenData if valid.

    Parameters
    ----------
    token: str
        The JWT token to be verified.
    db: AsyncSession
        Database session for performing database operations.

    Returns
    -------
    Optional[TokenData]
        TokenData instance if the token is valid, None otherwise.
    """
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username_or_email: str = payload.get("sub")

        if username_or_email is None:
            return None

        return TokenData(username_or_email=username_or_email)
    except Exception:
        # Handle invalid or expired tokens
        return None


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.

    Parameters
    ----------
    password: str
        The plain-text password to hash.

    Returns
    -------
    str
        The hashed password.
    """
    hashed_password: str = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return hashed_password
