from typing import List

import fastapi
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.base import DatasetCreate, Dataset
from schemas.user import User
from api.utils.bases import get_all_datalist, get_function_datalist, create_datalist, delete_datalist, update_datalist, get_function_datalist
from api.utils.oauth2 import get_current_user


router = fastapi.APIRouter(
    tags=["Dataset"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Dataset])
async def read_datalist(db: Session = Depends(get_db)):
    datalist = get_all_datalist(db)
    if not datalist:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Data not found.")
    return datalist


@router.get("/{function}", status_code=status.HTTP_200_OK, response_model=Dataset)
async def read_function(db: Session = Depends(get_db), function=str):
    result = get_function_datalist(db=db, function=function)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="function not found.")
    return result


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Dataset)
async def create_new_datalist(dataset: DatasetCreate, db: Session =Depends(get_db), current_user: User =Depends(get_current_user)):
    result = get_function_datalist(db=db, function=dataset.function)
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Function is already existed.")
    return create_datalist(db=db, base=dataset)


@router.patch("/{function}", status_code=status.HTTP_202_ACCEPTED, response_model=Dataset)
async def update_function(dataset: DatasetCreate, db: Session =Depends(get_db), current_user: User =Depends(get_current_user)):
    result = get_function_datalist(db=db, function=dataset.function)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Function not found.")
    return update_datalist(db=db, base=dataset)


@router.delete("/{function}", status_code=status.HTTP_202_ACCEPTED, response_model=Dataset)
async def delete_function(db: Session= Depends(get_db), function=str, current_user: User =Depends(get_current_user)):
    result = get_function_datalist(db=db, function=function)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Function not found.")
    return delete_datalist(db=db, function=function)