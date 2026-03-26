from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.member import Member
from app.services.wallet_service import add_wallet_tx
from app.services.settings_service import get_settings

def create_order(db: Session, channel: str, order_no: str | None, amount_gross: float, amount_paid: float,
                 member_id: int | None, use_referral: float, use_recharge: float, operator_user_id: int | None):
    if order_no:
        existing = db.query(Order).filter(Order.channel==channel, Order.order_no==order_no).first()
        if existing:
            return existing, False

    member = None
    if member_id:
        member = db.query(Member).filter(Member.id==member_id).first()
        if not member:
            raise ValueError("member_not_found")

    if member:
        if use_referral < 0 or use_recharge < 0:
            raise ValueError("invalid_wallet_use")
        if float(member.wallet_referral_balance) + 1e-6 < use_referral:
            raise ValueError("insufficient_referral_balance")
        if float(member.wallet_recharge_balance) + 1e-6 < use_recharge:
            raise ValueError("insufficient_recharge_balance")

        if use_referral > 0:
            member.wallet_referral_balance = float(member.wallet_referral_balance) - use_referral
            add_wallet_tx(db, member.id, "referral", "out", use_referral, "pay", None, operator_user_id)
        if use_recharge > 0:
            member.wallet_recharge_balance = float(member.wallet_recharge_balance) - use_recharge
            add_wallet_tx(db, member.id, "recharge", "out", use_recharge, "pay", None, operator_user_id)

        member.total_spent = float(member.total_spent) + float(amount_paid)

    s = get_settings(db)
    rate = float(s.referral_rate)

    referrer_id = None
    referral_amount = 0.0
    if member and member.referrer_member_id:
        referrer_id = member.referrer_member_id
        referral_amount = round(float(amount_paid) * rate, 2)  # 实付金额
        if referral_amount > 0:
            referrer = db.query(Member).filter(Member.id==referrer_id).first()
            if referrer and referrer.status == "active":
                referrer.wallet_referral_balance = float(referrer.wallet_referral_balance) + referral_amount
                referrer.referral_total_earned = float(referrer.referral_total_earned) + referral_amount
                add_wallet_tx(db, referrer.id, "referral", "in", referral_amount, "referral_earn", None, operator_user_id,
                              note=f"from_member:{member.id}")

    order = Order(channel=channel, order_no=order_no, amount_gross=amount_gross, amount_paid=amount_paid,
                  member_id=member.id if member else None, referrer_member_id=referrer_id,
                  referral_rate=rate, referral_amount=referral_amount,
                  wallet_referral_used=use_referral, wallet_recharge_used=use_recharge,
                  status="paid", is_refund=False)
    db.add(order); db.flush()
    return order, True

def refund_order(db: Session, order_id: int, operator_user_id: int | None, reason: str | None = None):
    order = db.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise ValueError("order_not_found")
    if order.status == "refunded":
        return order, False

    if order.member_id:
        member = db.query(Member).filter(Member.id==order.member_id).first()
        if member:
            if float(order.wallet_referral_used) > 0:
                member.wallet_referral_balance = float(member.wallet_referral_balance) + float(order.wallet_referral_used)
                add_wallet_tx(db, member.id, "referral", "in", float(order.wallet_referral_used), "refund", order.id, operator_user_id, note=reason)
            if float(order.wallet_recharge_used) > 0:
                member.wallet_recharge_balance = float(member.wallet_recharge_balance) + float(order.wallet_recharge_used)
                add_wallet_tx(db, member.id, "recharge", "in", float(order.wallet_recharge_used), "refund", order.id, operator_user_id, note=reason)

    if order.referrer_member_id and float(order.referral_amount) > 0:
        referrer = db.query(Member).filter(Member.id==order.referrer_member_id).first()
        if referrer:
            referrer.wallet_referral_balance = float(referrer.wallet_referral_balance) - float(order.referral_amount)
            referrer.referral_total_earned = float(referrer.referral_total_earned) - float(order.referral_amount)
            add_wallet_tx(db, referrer.id, "referral", "out", float(order.referral_amount), "refund", order.id, operator_user_id, note=f"reverse:{reason or ''}")

    order.status = "refunded"
    order.is_refund = True
    return order, True
