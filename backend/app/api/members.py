from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.session import get_db
from app.api.deps import get_current_user, require_owner
from app.schemas.member import MemberCreate, MemberOut, MemberSearchOut, TopupIn, TopupPromoOut
from app.models.member import Member
from app.services.wallet_service import add_wallet_tx
from app.services.settings_service import get_settings

router = APIRouter()

def ensure_contact(phone, email):
    if not phone and not email:
        raise HTTPException(status_code=400, detail="phone_or_email_required")

@router.get("", response_model=MemberSearchOut)
def list_members(q: str | None = Query(default=None), db: Session = Depends(get_db), user=Depends(get_current_user)):
    query = db.query(Member)
    if q:
        q = q.strip()
        query = query.filter(or_(Member.phone.ilike(f"%{q}%"), Member.email.ilike(f"%{q}%"), Member.name.ilike(f"%{q}%"), Member.ref_code.ilike(f"%{q}%")))
    items = query.order_by(Member.id.desc()).limit(50).all()
    return {"items": items}

@router.post("", response_model=MemberOut)
def create(data: MemberCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ensure_contact(data.phone, data.email)
    m = Member(phone=data.phone, email=(data.email.lower() if data.email else None), name=data.name)
    if data.ref_code:
        referrer = db.query(Member).filter(Member.ref_code==data.ref_code).first()
        if referrer and referrer.id != m.id:
            m.referrer_member_id = referrer.id
    db.add(m)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="duplicate_or_invalid")
    db.refresh(m)
    return m

@router.get("/{member_id}", response_model=MemberOut)
def get_member(member_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    m = db.query(Member).filter(Member.id==member_id).first()
    if not m: raise HTTPException(status_code=404, detail="Not found")
    return m

@router.post("/{member_id}/topup", response_model=MemberOut)
def topup(member_id: int, data: TopupIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    m = db.query(Member).filter(Member.id==member_id).first()
    if not m: raise HTTPException(status_code=404, detail="Not found")
    if data.amount <= 0: raise HTTPException(status_code=400, detail="Invalid amount")
    m.wallet_recharge_balance = float(m.wallet_recharge_balance) + float(data.amount)
    m.total_recharge = float(m.total_recharge) + float(data.amount)
    add_wallet_tx(db, m.id, "recharge", "in", float(data.amount), "recharge", None, user.id)
    db.commit(); db.refresh(m)
    return m

@router.post("/{member_id}/topup_promo_100_10", response_model=TopupPromoOut)
def topup_promo(member_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    m = db.query(Member).filter(Member.id==member_id).first()
    if not m: raise HTTPException(status_code=404, detail="Not found")
    s = get_settings(db)
    if not s.enable_topup_promo: raise HTTPException(status_code=400, detail="Promo disabled")
    charge = float(s.topup_charge_amount); bonus = float(s.topup_bonus_amount)
    m.wallet_recharge_balance = float(m.wallet_recharge_balance) + charge + bonus
    m.total_recharge = float(m.total_recharge) + charge
    m.total_bonus = float(m.total_bonus) + bonus
    add_wallet_tx(db, m.id, "recharge", "in", charge, "recharge", None, user.id, note="promo_charge")
    add_wallet_tx(db, m.id, "recharge", "in", bonus, "bonus", None, user.id, note="promo_bonus")
    db.commit(); db.refresh(m)
    return TopupPromoOut(recharge_added=charge, bonus_added=bonus, new_recharge_balance=float(m.wallet_recharge_balance))
