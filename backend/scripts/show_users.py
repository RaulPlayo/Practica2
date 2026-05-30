import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.repositories import UserRepository

if __name__ == '__main__':
    db = SessionLocal()
    admin = UserRepository.get_by_username(db, 'admin')
    user = UserRepository.get_by_username(db, 'usuario')
    print('admin:', admin.id if admin else None, admin.hashed_password if admin else None)
    print('usuario:', user.id if user else None, user.hashed_password if user else None)
    db.close()
