import uuid
from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from app.utils.refcode import generate_ref_code

class Member(Base):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    ref_code: Mapped[str] = mapped_column(String(16), unique=True, index=True, default=lambda: generate_ref_code())

    phone: Mapped[str | None] = mapped_column(String(32), unique=True, index=True, nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    name: Mapped[str | None] = mapped_column(String(120), nullable=True)

    status: Mapped[str] = mapped_column(String(16), default="active")

    referrer_member_id: Mapped[int | None] = mapped_column(ForeignKey("members.id"), nullable=True)
    referrer = relationship("Member", remote_side=[id], backref="referrals")

    wallet_recharge_balance: Mapped[float] = mapped_column(Numeric(12,2), default=0)
    wallet_referral_balance: Mapped[float] = mapped_column(Numeric(12,2), default=0)

    total_recharge: Mapped[float] = mapped_column(Numeric(12,2), default=0)
    total_bonus: Mapped[float] = mapped_column(Numeric(12,2), default=0)
    total_spent: Mapped[float] = mapped_column(Numeric(12,2), default=0)
    referral_total_earned: Mapped[float] = mapped_column(Numeric(12,2), default=0)
