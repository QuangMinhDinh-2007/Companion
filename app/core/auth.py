from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.supabase import get_db

bearer = HTTPBearer()

def get_current_user_id(
    cred: HTTPAuthorizationCredentials = Depends(bearer),
) -> str:
    """Verifies the Supabase JWT and returns the user's id."""
    try:
        resp = get_db().auth.get_user(cred.credentials)
    except Exception:
        resp = None
    if resp is None or resp.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return resp.user.id