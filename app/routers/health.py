from fastapi import APIRouter

from app.config import settings
from app.schemas.models import HealthResponse

router = APIRouter(tags=['health'])


@router.get('/health', response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(ok=True, vision_provider='openai' if settings.openai_api_key else 'mock')
