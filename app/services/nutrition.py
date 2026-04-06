from .food_db import COOKING, FOOD_DB, OIL, PORTION, SOURCE


def normalize_name(name: str) -> str | None:
    lowered = name.lower().strip()
    for key in FOOD_DB:
        if key in lowered or lowered in key:
            return key
    aliases = {
        'roti': 'chapati',
        'plain rice': 'rice',
        'boiled egg': 'egg',
        'chicken curry': 'chicken'
    }
    return aliases.get(lowered)


def adjusted_item(key: str, source: str, cooking: str, portion: str, oil: str) -> dict:
    base = FOOD_DB[key]
    multiplier = PORTION.get(portion, 1.0) * SOURCE.get(source, 1.0) * COOKING.get(cooking, 1.0) * OIL.get(oil, 1.0)
    return {
        'name': base['name'],
        'calories': round(base['calories'] * multiplier),
        'protein': round(base['protein'] * multiplier, 1),
        'carbs': round(base['carbs'] * multiplier, 1),
        'fat': round(base['fat'] * multiplier, 1),
        'base_qty': base['base_qty'],
    }


def summarise(items: list[dict]) -> dict:
    return {
        'calories': round(sum(item['calories'] for item in items)),
        'protein': round(sum(item['protein'] for item in items), 1),
        'carbs': round(sum(item['carbs'] for item in items), 1),
        'fat': round(sum(item['fat'] for item in items), 1),
    }
