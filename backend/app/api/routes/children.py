from fastapi import APIRouter, HTTPException, status

from app.models.api import ChildCreateRequest, MessageResponse

router = APIRouter(prefix="/children", tags=["children"])


@router.get("", response_model=MessageResponse, status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def list_children() -> MessageResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Children endpoints are planned for Phase 2.",
    )


@router.post("", response_model=MessageResponse, status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def create_child(_: ChildCreateRequest) -> MessageResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Children endpoints are planned for Phase 2.",
    )
