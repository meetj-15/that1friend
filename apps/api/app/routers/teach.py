from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.schemas.learning import LearningProfile
from app.services.model.ollama_provider import OllamaProvider
from app.services.teach import TeachService

router = APIRouter(prefix="/teach", tags=["teach"])
service = TeachService(OllamaProvider())


class TeachInput(BaseModel):
    topic: str = Field(min_length=2, max_length=300)
    time_budget_minutes: int | None = Field(default=None, ge=1, le=180)


@router.post("")
async def teach(payload: TeachInput):
    profile = LearningProfile()
    return await service.create_lesson(
        topic=payload.topic,
        profile=profile,
        time_budget_minutes=payload.time_budget_minutes,
    )
# Include in apps/api/app/main.py
from app.routers.teach import router as teach_router
app.include_router(teach_router)
