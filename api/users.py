from typing import List, Annotated

import fastapi
from fastapi import Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from pydantic import SecretStr, EmailStr

from db.database import get_db
from schemas.user import User, ShowUser

from api.utils.users import get_users, get_user_by_email, get_user_by_username, create_user_db, update_user_db, delete_user_db, verify_user_db
from api.utils.token import create_access_token

from api.utils.oauth2 import get_current_active_admin
from api.utils.hashing import Hash
from api.utils.utils import username_query, password_query



router = fastapi.APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ShowUser])
async def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User =Depends(get_current_active_admin)
    ):
    users = get_users(db, skip=skip, limit=limit)
    if not users:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Users not found.")
    return users


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    username: Annotated[str, username_query], 
    password: Annotated[SecretStr, password_query], 
    email: Annotated[EmailStr, Query(description="Verify email on this page by using PUT method. A real email address is unnecessary.")], 
    db: Session =Depends(get_db)
    ):
    result = get_user_by_username(db=db, username=username)
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is already existed. Please use another username.")
    result = get_user_by_email(db=db, email=email)
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered. Please use another email.")
    access_token = create_access_token(
        data={"sub": username}
        )
    create_user_db(db=db, username=username, password=password, email=email, role=2, token=access_token)
    return {"username": username, "email": email, "verify_token": access_token, "description": "Please verify email by using PUT method."}


@router.patch("/{username}", status_code=status.HTTP_202_ACCEPTED, response_model=ShowUser)
async def update_user(
    username: Annotated[str, Path(min_length=4, max_length=50)], 
    old_password: Annotated[SecretStr, password_query], 
    new_password: Annotated[SecretStr, password_query], 
    email: EmailStr, 
    db: Session =Depends(get_db)
    ):
    result_username = get_user_by_username(db=db, username=username)
    if result_username is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invaild username or password.")
    if not Hash.verify(hashed_password=result_username.password, plain_password=old_password.get_secret_value()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invaild username or password.")
    result_email = get_user_by_email(db=db, email=email)
    if result_email is None:
        return update_user_db(db=db, username=username, password=new_password, email=email)
    if result_email.username != result_username.username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered. Please use another email.")
    return update_user_db(db=db, username=username, password=new_password, email=email)


@router.put("/{email}", status_code=status.HTTP_202_ACCEPTED, response_model=ShowUser)
async def verify_email(
    email: Annotated[EmailStr, Path()], 
    token: Annotated[str, Query(description="Get your token by using POST login method before verify.")], 
    db: Session =Depends(get_db)
    ):
    result = get_user_by_email(db=db, email=email)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found.")
    if token == result.token:
        return verify_user_db(db=db, username=result.username, token=token, is_active=True)
    
    
@router.delete("/{username}", status_code=status.HTTP_202_ACCEPTED, response_model=User)
async def delete_user(
    username: Annotated[str, Path(min_length=4, max_length=50)], 
    db: Session= Depends(get_db), 
    current_user: User =Depends(get_current_active_admin)
    ):
    result = get_user_by_username(db=db, username=username)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found.")
    return delete_user_db(db=db, username=username)
