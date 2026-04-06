from pydantic import BaseModel, Field


class FoodItem(BaseModel):
    name: str
    calories: int
    protein: float
    carbs: float
    fat: float
    base_qty: str | None = None


class AnalysisRequest(BaseModel):
    source: str = Field(default='homemade')
    cooking: str = Field(default='boiled')
    portion: str = Field(default='medium')
    oil: str = Field(default='normal')


class AnalysisResponse(BaseModel):
    confidence: str
    confidence_score: float
    meal_type: str
    items: list[FoodItem]
    calories: int
    protein: float
    carbs: float
    fat: float
    calorie_range: list[int] | None = None
    notes: str


class HealthResponse(BaseModel):
    ok: bool
    vision_provider: str
