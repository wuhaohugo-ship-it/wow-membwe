from fastapi import APIRouter
from app.api import auth, members, orders, qrs, public

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(members.router, prefix="/members", tags=["members"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(qrs.router, prefix="/qr", tags=["qr"])
api_router.include_router(public.router, prefix="/public", tags=["public"])
