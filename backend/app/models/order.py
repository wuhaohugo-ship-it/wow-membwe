from sqlalchemy import String, ForeignKey, Numeric, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    channel: Mapped[str] = mapped_column(String(16))
    order_no: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)

    amount_gross: Mapped[float] = mapped_column(Numeric(12,2))
    amount_paid: Mapped[float] = mapped_column(Numeric(12,2))  # 实付金额

    member_id: Mapped[int | None] = mapped_column(ForeignKey("members.id"), nullable=True)
    member = relationship("Member")

    referrer_member_id: Mapped[int | None] = mapped_column(Integer, nullable=True)  # snapshot
    referral_rate: Mapped[float] = mapped_column(Numeric(5,4), default=0.10)
    referral_amount: Mapped[float] = mapped_column(Numeric(12,2), default=0)

    wallet_recharge_used: Mapped[float] = mapped_column(Numeric(12,2), default=0)
    wallet_referral_used: Mapped[float] = mapped_column(Numeric(12,2), default=0)

    status: Mapped[str] = mapped_column(String(16), default="paid")
    is_refund: Mapped[bool] = mapped_column(Boolean, default=False)
