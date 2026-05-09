from fastapi import APIRouter, HTTPException, Path, status

from app.models.api import MessageResponse, StoryGenerateRequest

router = APIRouter(prefix="/stories", tags=["stories"])


@router.post("/generate", response_model=MessageResponse, status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def generate_story(_: StoryGenerateRequest) -> MessageResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Story generation endpoint is planned for Phase 3.",
    )


@router.get("/history", response_model=MessageResponse, status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def list_story_history() -> MessageResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Story history endpoint is planned for Phase 5.",
    )


@router.post(
    "/{story_id}/regenerate",
    response_model=MessageResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
)
async def regenerate_story(story_id: str = Path(...)) -> MessageResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Regenerate endpoint for story '{story_id}' is planned for Phase 6.",
    )
