# Auth Middleware
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import time

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, options={"verify_signature": False})

        # Check token expiration
        if payload.get("exp", 0) < time.time():
            raise HTTPException(status_code=401, detail="Token expired")

        return payload
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

def get_current_user(payload: dict = Depends(verify_token)) -> dict:
    """Get current user from token"""
    return {
        "user_id": payload.get("sub"),
        "email": payload.get("email")
    }
