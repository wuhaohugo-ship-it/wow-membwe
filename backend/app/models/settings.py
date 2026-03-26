from sqlalchemy import Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class AppSettings(Base):
    __tablename__ = "app_settings"
    id: Mapped[int] = mapped_column(primary_key=True)
    referral_rate: Mapped[float] = mapped_column(Numeric(5,4), default=0.10)
    topup_charge_amount: Mapped[float] = mapped_column(Numeric(12,2), default=100.00)
    topup_bonus_amount: Mapped[float] = mapped_column(Numeric(12,2), default=10.00)
    enable_topup_promo: Mapped[bool] = mapped_column(Boolean, default=True)
