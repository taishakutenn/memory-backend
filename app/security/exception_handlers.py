from fastapi import Request, status
from fastapi.responses import JSONResponse


async def credentials_exception(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Could not validate credentials"},
        headers={"WWW-Authenticate": "Bearer"}
    )


async def inactive_user(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "Inactive user"},
    )


async def user_unauthorized(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Incorrect username or password"},
        headers={"WWW-Authenticate": "Bearer"},
    )