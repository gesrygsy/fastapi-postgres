from typing import List, Annotated

import fastapi
from fastapi import Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session

from db.database import get_db
from db.models.base import SymbolType
from schemas.base import Dataset
from schemas.user import User
from api.utils.bases import get_all_datalist, get_function_datalist, create_datalist, delete_datalist, update_datalist, get_function_datalist
from api.utils.currencies import get_currency
from api.utils.oauth2 import get_current_active_admin
from api.utils.utils import function_query


router = fastapi.APIRouter(
    tags=["Dataset"],
    prefix="/dataset",
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Dataset])
async def read_datalist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
    ):
    datalist = get_all_datalist(db)
    if not datalist:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Data not found.")
    return datalist


@router.get("/{function}", status_code=status.HTTP_200_OK, response_model=Dataset)
async def read_function(
    function: Annotated[str, Path(max_length=100)], 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
    ):
    result = get_function_datalist(db=db, function=function)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="function not found.")
    return result


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Dataset)
async def create_new_datalist(
    function: Annotated[str, function_query], 
    type: str = Query(enum=list(SymbolType)), 
    description: str = None, 
    data_source: Annotated[str, Query(max_length=100)] = None, 
    db: Session =Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
    ):
    result = get_function_datalist(db=db, function=function)
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Function is already existed.")
    return create_datalist(db=db, function=function, type=type, description=description, data_source=data_source)


@router.patch("/{function}", status_code=status.HTTP_202_ACCEPTED, response_model=Dataset)
async def update_function(
    function: Annotated[str, Path(max_length=100)],
    type: str = Query(enum=list(SymbolType)),
    description: str = None,
    data_source: str = None, 
    db: Session =Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
    ):
    result = get_function_datalist(db=db, function=function)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Function not found.")
    return update_datalist(db=db, type=type, description=description, data_source=data_source, to_be_update=result)


@router.delete("/{function}", status_code=status.HTTP_202_ACCEPTED, response_model=Dataset)
async def delete_function(
    function: Annotated[str, Path(max_length=100)], 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_admin)
    ):
    result = get_function_datalist(db=db, function=function)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Function not found.")
    result = get_currency(db=db, skip=0, limit=10)
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Function data existed. Please remove all Function data before delete Function.")
    return delete_datalist(db=db, function=function)