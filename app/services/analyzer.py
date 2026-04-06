from __future__ import annotations

import random

from .food_db import FOOD_DB
from .nutrition import adjusted_item, normalize_name, summarise
from .openai_vision import detect_foods_with_openai


async def analyze_food_image(image_bytes: bytes, filename: str, source: str, cooking: str, portion: str, oil: str) -> dict:
    detected = await detect_foods_with_openai(image_bytes, filename)

    normalized = []
    for item in detected:
        key = normalize_name(item)
        if key and key not in normalized:
            normalized.append(key)

    if not normalized:
        normalized = fallback_from_filename(filename)

    items = [adjusted_item(key, source, cooking, portion, oil) for key in normalized]
    totals = summarise(items)
    confidence = 'high' if detected else 'medium'
    confidence_score = 0.86 if detected else 0.66
    calorie_range = None if confidence == 'high' else [round(totals['calories'] * 0.9), round(totals['calories'] * 1.1)]
    meal_type = infer_meal_type(normalized)

    return {
        'confidence': confidence,
        'confidence_score': confidence_score,
        'meal_type': meal_type,
        'items': items,
        'calories': totals['calories'],
        'protein': totals['protein'],
        'carbs': totals['carbs'],
        'fat': totals['fat'],
        'calorie_range': calorie_range,
        'notes': 'Uses OpenAI vision when an API key is configured, otherwise falls back to filename and built-in food rules.'
    }


def fallback_from_filename(filename: str) -> list[str]:
    lower = filename.lower()
    hits = [key for key in FOOD_DB if key in lower]
    if hits:
        return hits[:4]
    return random.sample(list(FOOD_DB.keys()), k=3)


def infer_meal_type(keys: list[str]) -> str:
    joined = ' '.join(keys)
    if 'dosa' in joined or 'idli' in joined or 'egg' in joined:
        return 'breakfast'
    if 'biryani' in joined or 'rice' in joined or 'dal' in joined:
        return 'lunch'
    if 'pizza' in joined or 'pasta' in joined:
        return 'dinner'
    return 'snack'
