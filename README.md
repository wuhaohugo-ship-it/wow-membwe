# WOW Members System MVP
- PostgreSQL + FastAPI backend
- React admin
- QR generation (member + referral)
- Promo: 100€ + 10€
- Referral cashback: 10% over **amount_paid** (实付金额)

## Start
```bash
docker compose up -d db
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python seed.py
uvicorn main:app --reload --port 8000
```

Frontend:
```bash
cd ../frontend
npm install
npm run dev
```
