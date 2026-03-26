from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.member import Member

router = APIRouter()

@router.get("/join", response_class=HTMLResponse)
def join_page(ref: str | None = Query(default=None)):
    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>WOW · Hazte socio</title><style>
body{{font-family:Arial;margin:0;background:#fff;color:#111}}
.wrap{{max-width:520px;margin:0 auto;padding:18px}}
.card{{border:1px solid #eee;border-radius:14px;padding:16px}}
input{{width:100%;padding:12px;border:1px solid #ddd;border-radius:10px;margin:8px 0}}
button{{width:100%;padding:12px;border-radius:10px;border:1px solid #111;background:#111;color:#fff;font-weight:700}}
small{{color:#666}}</style></head><body><div class="wrap">
<h2>Hazte socio · WOW</h2><div class="card">
<small>Introduce tu teléfono o email. {('Ref: '+ref) if ref else ''}</small>
<form method="post" action="/api/public/register">
<input name="phone" placeholder="Teléfono (opcional)">
<input name="email" placeholder="Email (opcional)">
<input name="name" placeholder="Nombre (opcional)">
<input type="hidden" name="ref_code" value="{ref or ''}">
<button type="submit">Crear cuenta</button></form>
<p><small>Saldo promocional no canjeable por dinero. Solo para consumir en el local.</small></p>
</div></div></body></html>"""
    return html

@router.post("/register")
def register_member(phone: str | None = None, email: str | None = None, name: str | None = None, ref_code: str | None = None,
                    db: Session = Depends(get_db)):
    if not phone and not email:
        raise HTTPException(status_code=400, detail="phone_or_email_required")
    m = Member(phone=phone.strip() if phone else None, email=email.lower().strip() if email else None, name=name)
    if ref_code:
        referrer = db.query(Member).filter(Member.ref_code==ref_code).first()
        if referrer and referrer.id != m.id:
            m.referrer_member_id = referrer.id
    db.add(m)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="duplicate_or_invalid")
    db.refresh(m)
    return {"id": m.id, "public_id": m.public_id, "ref_code": m.ref_code}

@router.get("/m/{public_id}", response_class=HTMLResponse)
def member_page(public_id: str, db: Session = Depends(get_db)):
    m = db.query(Member).filter(Member.public_id==public_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Not found")
    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>WOW · Socio</title><style>
body{{font-family:Arial;margin:0;background:#fff;color:#111}}
.wrap{{max-width:520px;margin:0 auto;padding:18px}}
.card{{border:1px solid #eee;border-radius:14px;padding:16px}}
.badge{{display:inline-block;padding:6px 10px;border:1px solid #111;border-radius:999px;font-weight:700;font-size:12px}}
.row{{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px dashed #eee}}
.row:last-child{{border-bottom:none}}</style></head><body><div class="wrap">
<div class="badge">WOW BAR RESTAURANTE</div><h2>Tu cuenta</h2>
<div class="card">
<div class="row"><strong>Saldo recarga</strong><span>€ {float(m.wallet_recharge_balance):.2f}</span></div>
<div class="row"><strong>Saldo recomendación</strong><span>€ {float(m.wallet_referral_balance):.2f}</span></div>
<div class="row"><strong>Código recomendación</strong><span>{m.ref_code}</span></div>
<p style="color:#666;font-size:12px">Muestra este QR en caja para identificar tu cuenta.</p>
<img style="width:100%;max-width:320px" src="/api/qr/member/{m.public_id}.png" alt="QR">
</div></div></body></html>"""
    return html
