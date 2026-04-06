from __future__ import annotations

import base64
import json
from typing import Any

import httpx

from app.config import settings

SYSTEM_PROMPT = (
    'You are a food recognition assistant. '
    'Look at the food image and return a JSON object with a single key "foods" whose value is an array of short food names. '
    'Use simple names only, like rice, dal, biryani, chapati, egg, chicken, paneer, dosa, idli, salad, pizza, pasta. '
    'Do not include text outside the JSON.'
)


async def detect_foods_with_openai(image_bytes: bytes, filename: str | None = None) -> list[str]:
    if not settings.openai_api_key:
        return []

    image_b64 = base64.b64encode(image_bytes).decode('utf-8')
    headers = {
        'Authorization': f'Bearer {settings.openai_api_key}',
        'Content-Type': 'application/json',
    }
    payload: dict[str, Any] = {
        'model': settings.openai_model,
        'input': [
            {
                'role': 'system',
                'content': [{'type': 'input_text', 'text': SYSTEM_PROMPT}],
            },
            {
                'role': 'user',
                'content': [
                    {'type': 'input_text', 'text': f'Analyze this food photo. File name: {filename or "upload"}.'},
                    {
                        'type': 'input_image',
                        'image_url': f'data:image/jpeg;base64,{image_b64}',
                        'detail': 'high',
                    },
                ],
            },
        ],
    }

    async with httpx.AsyncClient(timeout=45) as client:
        response = await client.post('https://api.openai.com/v1/responses', headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    text = extract_text(data)
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return []

    foods = parsed.get('foods') if isinstance(parsed, dict) else []
    if not isinstance(foods, list):
        return []
    return [str(item).strip().lower() for item in foods if str(item).strip()]


def extract_text(data: dict[str, Any]) -> str:
    output = data.get('output', [])
    chunks: list[str] = []
    for item in output:
        for content in item.get('content', []):
            text = content.get('text')
            if text:
                chunks.append(text)
    return ''.join(chunks).strip()
