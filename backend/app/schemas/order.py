from pydantic import BaseModel
from typing import Optional

class OrderCreate(BaseModel):
    channel: str
    order_no: Optional[str] = None
    amount_gross: float
    amount_paid: float
    member_id: Optional[int] = None
    use_wallet_referral: float = 0
    use_wallet_recharge: float = 0

class OrderOut(BaseModel):
    id: int
    channel: str
    order_no: Optional[str]
    amount_gross: float
    amount_paid: float
    member_id: Optional[int]
    referrer_member_id: Optional[int]
    referral_rate: float
    referral_amount: float
    wallet_recharge_used: float
    wallet_referral_used: float
    status: str
    class Config:
        from_attributes = True

class RefundIn(BaseModel):
    reason: Optional[str] = None
