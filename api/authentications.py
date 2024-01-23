from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr, EmailStr
import fastapi

from db.database import get_db
from api.utils.hashing import Hash
from api.utils.users import get_user_by_username
# from api.utils.token import create_access_token
from schemas.authentication import Login

from api.utils.users import create_user_db, get_user_by_username, get_user_by_email
from api.utils.utils import username_query, password_query
from api.utils.oauth2 import SYSTEM_PASSWORD
from api.utils.token import create_access_token


router = fastapi.APIRouter(
    tags=["Authentication"],
)


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login(request: OAuth2PasswordRequestForm =Depends(Login), db: Session =Depends(get_db)):
    user = get_user_by_username(db=db, username=request.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password") 
    if not Hash.verify(hashed_password=user.password, plain_password=request.password.get_secret_value()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password.", headers={"WWW-Authenticate": "Bearer"})
    if not user.is_active:
        return {"access_token": user.token, "description": "Inactive. Please verify email by using PUT method."}
    else:
        return {"access_token": user.token, "description": "Email verified."}
    # access_token = create_access_token(
    #     data={"sub": user.username}
    #     )


@router.post("/admin", status_code=status.HTTP_201_CREATED)
async def create_admin(
    system_password: Annotated[SecretStr, Query(description="Please enter system password.")],
    username: Annotated[str, username_query],
    email: Annotated[EmailStr, Query(description="Verify email on this page by using PUT method. A real email address is unnecessary.")], 
    password: Annotated[SecretStr, password_query],
    db: Session =Depends(get_db),
):
    if system_password.get_secret_value() != SYSTEM_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong system password.")
    result = get_user_by_username(db=db, username=username)
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is already existed. Please use another username.")
    result = get_user_by_email(db=db, email=email)
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered. Please use another email.")
    access_token = create_access_token(
        data={"sub": username}
        )
    create_user_db(db=db, username=username, password=password, email=email, role=1, token=access_token)
    return {"username": username, "email": email, "verify_token": access_token, "description": "Please verify email by using PUT method."}