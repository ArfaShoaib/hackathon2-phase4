from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, ExpiredSignatureError, JWTError
from typing import Dict, Any
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get JWT configuration from environment (for Better Auth system)
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", os.getenv("SECRET_KEY", "your-default-secret-key-change-in-production"))
ALGORITHM = "HS256"  # Better Auth uses HS256 by default

security = HTTPBearer()


def verify_jwt_token(token: str) -> Dict[str, Any]:
    """
    Verify the JWT token and return the decoded claims using Better Auth configuration.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token provided",
        )

    print(f"DEBUG: Attempting to verify token with secret key: {SECRET_KEY[:10]}...")  # Debug print
    
    # Verify the token using Better Auth secret key with HS256 algorithm
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except JWTError as e:
        print(f"DEBUG: JWT Error: {str(e)}")  # Debug print
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
        )

    print(f"DEBUG: Token payload: {payload}")  # Debug print
    return payload


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency function to get the current authenticated user from Better Auth JWT.
    """
    token = credentials.credentials
    payload = verify_jwt_token(token)

    # Extract user information from the token payload
    user_id = payload.get("sub")
    print(f"DEBUG: Token payload: {payload}")
    print(f"DEBUG: Token sub field: {user_id} (type: {type(user_id)})")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    # Try to convert to int, but handle string IDs as well
    try:
        user_id_int = int(user_id)
        print(f"DEBUG: Successfully converted user_id to int: {user_id_int}")
        return {"user_id": user_id_int}
    except (ValueError, TypeError):
        print(f"DEBUG: Could not convert user_id to int: {user_id}. Returning as string.")
        # If it's not an integer, return as string - this might be an email or UUID from Better Auth
        return {"user_id": str(user_id)}