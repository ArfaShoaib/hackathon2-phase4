from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Optional
import os
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# Initialize JWT configuration from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


class JWTBearer(HTTPBearer):
    """
    Custom JWT Bearer authentication scheme that validates JWT tokens.
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, credentials: HTTPAuthorizationCredentials = None):
        """
        Validate the JWT token from the Authorization header.

        Args:
            credentials: The authorization credentials from the header

        Returns:
            Token payload if valid

        Raises:
            HTTPException: If token is invalid or expired
        """
        if credentials is None or not credentials.credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = credentials.credentials
        return verify_jwt_token(token)


def verify_jwt_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return the payload if valid.

    Args:
        token: The JWT token to verify

    Returns:
        Token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user_id from JWT token.

    Args:
        token: The JWT token

    Returns:
        User ID if token is valid, None otherwise
    """
    payload = verify_jwt_token(token)
    return payload.get("sub")  # assuming "sub" is where user_id is stored


def validate_user_ownership(token_user_id: str, request_user_id: str) -> bool:
    """
    Validate that the authenticated user can access resources for the specified user.

    Args:
        token_user_id: The user ID from the JWT token
        request_user_id: The user ID from the request path

    Returns:
        True if user IDs match, False otherwise
    """
    return token_user_id == request_user_id