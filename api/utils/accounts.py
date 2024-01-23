from datetime import datetime

from sqlalchemy.orm import Session

from db.models.account import Accounts
from schemas.account import AccountCreate
from .hashing import Hash


def get_accounts(db: Session, owner: str, skip: int = 0, limit: int = 100):
    return db.query(Accounts).filter(Accounts.owner_name == owner).offset(skip).limit(limit).all()


def create_account_db(db: Session, base: AccountCreate, user: str, id: int, email: str):
    db_account = Accounts(
        name=base.name,
        account=base.account,
        server=base.server, 
        password=Hash.bcrypt(base.password),
        owner_id=id,
        owner_name=user,
        owner_email=email,
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def get_account(db: Session, name: str, account: str, server: str, owner_name: str):
    return db.query(Accounts).filter((Accounts.name == name) & (Accounts.account == account) & (Accounts.server == server) & (Accounts.owner_name == owner_name)).first()


def update_account_db(db: Session, new_name: str, new_account: str, new_server: str, new_password: str, account_to_be_update):
    update = account_to_be_update

    update.name = new_name
    update.account = new_account
    update.server = new_server
    update.password = Hash.bcrypt(new_password)
    
    update.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(update)
    return update


def delete_account_db(db: Session, to_be_delete):
    db.delete(to_be_delete)
    db.commit()
    return to_be_delete