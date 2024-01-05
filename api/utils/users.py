from sqlalchemy.orm import Session

from db.models.user import User
from schemas.user import UserCreate
from .hashing import Hash


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_account(db: Session, base: UserCreate):
    db_user = User(
        username=base.username,
        email=base.email, 
        password=Hash.bcrypt(base.password),
        role=base.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_account(db: Session, base: UserCreate):
    update = db.query(User).filter(User.username == base.username).first()
    update.email = base.email
    update.password = Hash.bcrypt(base.password)
    update.role = base.role

    db.commit()
    db.refresh(update)
    return update


def delete_account(db: Session, username: str):
    result = db.query(User).filter(User.username == username).first()
    db.delete(result)
    db.commit()
    return result