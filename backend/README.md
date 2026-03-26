# Backend (FastAPI + PostgreSQL)

## Start Postgres
From project root:
```bash
docker compose up -d db
```

## Run backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env (DATABASE_URL, JWT_SECRET, BASE_URL)
python seed.py
uvicorn main:app --reload --port 8000
```

Docs: http://localhost:8000/docs
