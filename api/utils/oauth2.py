from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# from api.utils.token import verify_token
from api.utils.users import get_user_by_token
from db.database import get_db
from db.models.user import User


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SYSTEM_PASSWORD = "password"


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: str, db: Session =Depends(get_db)):
    current_user = get_user_by_token(db=db, token=token)
    if not current_user:
        raise credentials_exception
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user. Please verify your email.")
    # return verify_token(token, credentials_exception)
    return current_user


async def get_current_active_user(current_user: User =Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user. Please verify email.")
    return current_user


async def get_current_active_admin(current_user: User =Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive admin. Please verify email.")
    if current_user.role != 1:
        raise HTTPException(status_code=400, detail="You do not have permission. Please login as admininstrator.")
    return current_user
