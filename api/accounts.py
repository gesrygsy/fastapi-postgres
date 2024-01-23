from typing import List, Annotated

import fastapi
from fastapi import Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.user import User
from schemas.account import AccountCreate, ShowAccount, AccountUpdate

from api.utils.users import get_user_by_username
from api.utils.accounts import get_accounts, create_account_db, get_account, update_account_db, delete_account_db

from api.utils.oauth2 import get_current_active_user


router = fastapi.APIRouter(
    prefix="/account",
    tags=["Account"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ShowAccount])
async def get_all_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User =Depends(get_current_active_user)):
    accounts = get_accounts(db, owner=current_user.username, skip=skip, limit=limit)
    if not accounts:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No accounts exist.")
    return accounts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AccountCreate)
async def create_account(
    base: AccountCreate, 
    db: Session =Depends(get_db), 
    current_user: User =Depends(get_current_active_user)
    ):
    result = get_account(db=db, name=base.name, account=base.account, server=base.server, owner_name=base.owner_name)
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Same account existed. Please change your account name.")
    result = get_user_by_username(db=db, username=base.owner_name)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not existed.")
    return create_account_db(db=db, base=base, user=result.username, id=result.id, email=result.email)


@router.patch("/{name}", status_code=status.HTTP_202_ACCEPTED, response_model=ShowAccount)
async def update_account(
    base: AccountUpdate, 
    db: Session =Depends(get_db), 
    current_user: User =Depends(get_current_active_user)
    ):
    result_account = get_account(db=db, name=base.name, account=base.account, server=base.server, owner_name=base.owner_name)
    if result_account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found. Please make sure you are enter a valid account information.")
    return update_account_db(db=db, new_name=base.new_name, new_account=base.new_account, new_server=base.new_server, new_password=base.new_password, account_to_be_update=result_account)


@router.delete("/{name}", status_code=status.HTTP_202_ACCEPTED, response_model=ShowAccount)
async def delete_account(
    name: Annotated[str, Path(min_length=5, max_length=100)], 
    account: Annotated[str, Query(max_length=50)], 
    server: Annotated[str, Query(max_length=100)], 
    owner_name: Annotated[str, Query(description="Enter your username.")], 
    db: Session= Depends(get_db), 
    current_user: User =Depends(get_current_active_user)
    ):
    result_account = get_account(db=db, name=name, account=account, server=server, owner_name=owner_name)
    if result_account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found. Please make sure you are enter a valid account information.")
    return delete_account_db(db=db, to_be_delete=result_account)