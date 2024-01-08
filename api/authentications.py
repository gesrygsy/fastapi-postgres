from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import fastapi

from db.database import get_db
from api.utils.hashing import Hash
from api.utils.users import get_user_by_username
from api.utils.token import create_access_token


router = fastapi.APIRouter(
    tags=["Authentication"],
)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: OAuth2PasswordRequestForm =Depends(), db: Session =Depends(get_db)):
    user = get_user_by_username(db=db, username=request.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")    
    if not Hash.verify(hashed_password=user.password, plain_password=request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password.", headers={"WWW-Authenticate": "Bearer"})
    
    access_token = create_access_token(
        data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
