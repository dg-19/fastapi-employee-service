from database import SessionLocal
from models import User
from auth.auth import hash_password

db = SessionLocal()

# user = User(
#     email="john@test.com",
#     password_hash=hash_password("password123"),
#     is_active=True
# )

user = User(
    email="admin@test.com",
    password_hash=hash_password("admin123"),
    is_active=True,
    role="admin"
)

db.add(user)
db.commit()
db.refresh(user)

print(user.id, user.email)

db.close()