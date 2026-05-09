from fastapi import APIRouter, HTTPException, status

from app.models.api import LoginRequest, MessageResponse, RegisterRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def register(_: RegisterRequest) -> MessageResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Register endpoint is planned for Phase 1.",
    )


@router.post("/login", response_model=MessageResponse, status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def login(_: LoginRequest) -> MessageResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Login endpoint is planned for Phase 1.",
    )
