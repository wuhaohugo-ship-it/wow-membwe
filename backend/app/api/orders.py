from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.order import OrderCreate, OrderOut, RefundIn
from app.services.order_service import create_order, refund_order

router = APIRouter()

@router.post("", response_model=OrderOut)
def create(data: OrderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        order, created = create_order(db, data.channel, data.order_no, data.amount_gross, data.amount_paid,
                                      data.member_id, data.use_wallet_referral, data.use_wallet_recharge, user.id)
        db.commit(); db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{order_id}/refund", response_model=OrderOut)
def refund(order_id: int, data: RefundIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        order, changed = refund_order(db, order_id, user.id, data.reason)
        db.commit(); db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
