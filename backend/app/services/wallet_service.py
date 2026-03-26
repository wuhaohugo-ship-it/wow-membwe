from sqlalchemy.orm import Session
from app.models.wallet_tx import WalletTransaction
def add_wallet_tx(db: Session, member_id: int, wallet_type: str, direction: str, amount: float, reason: str,
                  order_id: int | None, operator_user_id: int | None, note: str | None = None):
    tx = WalletTransaction(member_id=member_id, wallet_type=wallet_type, direction=direction, amount=amount,
                           reason=reason, order_id=order_id, operator_user_id=operator_user_id, note=note)
    db.add(tx); db.flush()
    return tx
