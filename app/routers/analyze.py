from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.models import AnalysisResponse
from app.services.analyzer import analyze_food_image

router = APIRouter(prefix='/api', tags=['analysis'])


@router.post('/analyze', response_model=AnalysisResponse)
async def analyze(
    image: UploadFile = File(...),
    source: str = Form('homemade'),
    cooking: str = Form('boiled'),
    portion: str = Form('medium'),
    oil: str = Form('normal'),
) -> AnalysisResponse:
    contents = await image.read()
    result = await analyze_food_image(contents, image.filename or 'upload.jpg', source, cooking, portion, oil)
    return AnalysisResponse(**result)
