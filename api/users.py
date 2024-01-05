from typing import List

import fastapi
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.user import UserCreate, User, ShowUser
from api.utils.users import get_users, get_user_by_email, get_user_by_username, create_account, update_account, delete_account
from api.utils.oauth2 import get_current_user

router = fastapi.APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ShowUser])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User =Depends(get_current_user)):
    users = get_users(db, skip=skip, limit=limit)
    if not users:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Users not found.")
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(base: UserCreate, db: Session =Depends(get_db), current_user: User =Depends(get_current_user)):
    result = get_user_by_username(db=db, username=base.username)
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is already existed.")
    result = get_user_by_email(db=db, email=base.email)
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already existed.")
    return create_account(db=db, base=base)


@router.patch("/{username}", status_code=status.HTTP_202_ACCEPTED, response_model=User)
async def update_user(base: UserCreate, db: Session =Depends(get_db), current_user: User =Depends(get_current_user)):
    result_username = get_user_by_username(db=db, username=base.username)
    if result_username is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found.")
    result_email = get_user_by_email(db=db, email=base.email)
    if result_email.username != result_username.username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already existed. Please use another email.")
    return update_account(db=db, base=base)


@router.delete("/{username}", status_code=status.HTTP_202_ACCEPTED, response_model=User)
async def delete_user(db: Session= Depends(get_db), username=str, current_user: User =Depends(get_current_user)):
    result = get_user_by_username(db=db, username=username)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found.")
    return delete_account(db=db, username=username)