from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class MemberCreate(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    ref_code: Optional[str] = None

    @field_validator("phone","email")
    @classmethod
    def strip(cls, v):
        return v.strip() if isinstance(v,str) else v

class MemberOut(BaseModel):
    id: int
    public_id: str
    ref_code: str
    phone: Optional[str]
    email: Optional[str]
    name: Optional[str]
    status: str
    referrer_member_id: Optional[int]
    wallet_recharge_balance: float
    wallet_referral_balance: float
    class Config:
        from_attributes = True

class MemberSearchOut(BaseModel):
    items: list[MemberOut]

class TopupIn(BaseModel):
    amount: float

class TopupPromoOut(BaseModel):
    recharge_added: float
    bonus_added: float
    new_recharge_balance: float
