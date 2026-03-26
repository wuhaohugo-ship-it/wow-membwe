from sqlalchemy.orm import Session
from app.models.settings import AppSettings
def get_settings(db: Session) -> AppSettings:
    s = db.query(AppSettings).first()
    if not s:
        s = AppSettings()
        db.add(s); db.flush()
    return s
