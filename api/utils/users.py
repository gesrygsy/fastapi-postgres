from datetime import datetime

from sqlalchemy.orm import Session
from pydantic import EmailStr, SecretStr

from db.models.user import User
from .hashing import Hash


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_token(db: Session, token: str):
    return db.query(User).filter(User.token == token).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user_db(db: Session, username: str, password: SecretStr, email: EmailStr, role: int, token: str):
    db_user = User(
        username=username,
        email=email, 
        password=Hash.bcrypt(password.get_secret_value()),
        role=role,
        token=token,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_db(db: Session, username: str, password: SecretStr, email: EmailStr):
    update = db.query(User).filter(User.username == username).first()

    update.email = email
    update.password = Hash.bcrypt(password.get_secret_value())
    update.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(update)
    return update


def verify_user_db(db: Session, username: str, token: str, is_active: bool =False):
    update = db.query(User).filter(User.username == username).first()

    update.is_active = is_active
    update.token = token
    update.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(update)
    return update


def delete_user_db(db: Session, username: str):
    result = db.query(User).filter(User.username == username).first()
    db.delete(result)
    db.commit()
    return result
