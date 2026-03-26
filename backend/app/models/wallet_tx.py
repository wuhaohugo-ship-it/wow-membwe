from sqlalchemy import String, Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    wallet_type: Mapped[str] = mapped_column(String(16))  # recharge/referral
    direction: Mapped[str] = mapped_column(String(8))  # in/out
    amount: Mapped[float] = mapped_column(Numeric(12,2))
    reason: Mapped[str] = mapped_column(String(24))  # recharge/bonus/referral_earn/pay/refund/adjust
    order_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    operator_user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)
