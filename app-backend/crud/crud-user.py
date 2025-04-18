from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import uuid4
from models.models import User
from schemas.schemas import UserCreate


# Create User
def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
