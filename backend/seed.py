from sqlalchemy.orm import Session
from app.db.session import SessionLocal, init_db
from app.models.user import User
from app.core.security import hash_password

def run():
    init_db()
    db: Session = SessionLocal()
    try:
        if not db.query(User).filter(User.username=="owner").first():
            db.add(User(username="owner", password_hash=hash_password("owner1234"), role="owner"))
        if not db.query(User).filter(User.username=="staff").first():
            db.add(User(username="staff", password_hash=hash_password("staff1234"), role="staff"))
        db.commit()
        print("Seeded users: owner/owner1234, staff/staff1234")
    finally:
        db.close()

if __name__ == "__main__":
    run()
