# PlateCal AI Backend

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

If `OPENAI_API_KEY` is set, `/api/analyze` uses the OpenAI Responses API with image input.
If it is not set, the backend falls back to rule-based detection using the file name and built-in foods.
