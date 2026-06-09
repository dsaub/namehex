from fastapi import HTTPException, status
INVALID_LOGIN = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Invalid Username/Password"
)