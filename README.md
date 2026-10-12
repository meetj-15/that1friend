# That1Friend

A regional conversational AI friend with adaptive teaching, selective retrieval, memory, web research, YouTube recommendations and optional generated explainers.

## Architecture

Next.js -> FastAPI -> Adaptive Orchestrator -> Model Provider
                                  |
                Memory / Knowledge / Web / YouTube

## Local setup

### Web

cd apps/web
npm install
npm run dev

### API

cd apps/api
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload

## Current phase

Phase 14 - evaluation + deployment

## Rules

- Do not commit secrets.
- Keep the local model path working.
- Measure before fine-tuning.
- Do not run web retrieval for every chat message.
