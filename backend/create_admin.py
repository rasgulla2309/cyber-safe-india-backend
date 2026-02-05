from app.database import SessionLocal
from app.models.user import User
from app.utils.security import hash_password

db = SessionLocal()

username = "admin"
password = "admin@123"
role = "admin"

existing = db.query(User).filter(User.username == username).first()
if existing:
    print("❌ Admin already exists")
else:
    admin = User(
        username=username,
        password=hash_password(password),
        role=role
    )
    db.add(admin)
    db.commit()
    print("✅ Admin created successfully")

db.close()
