from __future__ import annotations

import httpx

from app.config import settings


async def search_usda_food(food_name: str) -> dict | None:
    if not settings.usda_api_key:
        return None

    url = 'https://api.nal.usda.gov/fdc/v1/foods/search'
    params = {
        'api_key': settings.usda_api_key,
        'query': food_name,
        'pageSize': 1,
    }
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    foods = data.get('foods') or []
    if not foods:
        return None
    return foods[0]
