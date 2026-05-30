import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.security import verify_password
from app.core.database import SessionLocal
from app.repositories import UserRepository

if __name__ == '__main__':
    db = SessionLocal()
    admin = UserRepository.get_by_username(db, 'admin')
    print('hashed:', admin.hashed_password)
    print('verify admin123:', verify_password('admin123', admin.hashed_password))
    print('verify admin:', verify_password('admin', admin.hashed_password))
    db.close()
