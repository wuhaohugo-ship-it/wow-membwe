from fastapi import APIRouter
from fastapi.responses import Response
from app.core.settings import settings
from app.utils.qr import make_qr_png

router = APIRouter()

@router.get("/member/{public_id}.png")
def qr_member(public_id: str):
    url = f"{settings.BASE_URL.rstrip('/')}/m/{public_id}"
    return Response(content=make_qr_png(url), media_type="image/png")

@router.get("/ref/{ref_code}.png")
def qr_ref(ref_code: str):
    url = f"{settings.BASE_URL.rstrip('/')}/join?ref={ref_code}"
    return Response(content=make_qr_png(url), media_type="image/png")
