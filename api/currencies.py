from typing import List, Annotated
from datetime import datetime
from dateutil.parser import parse

import fastapi
from fastapi import Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.currency import Currn, CurrnCreate, CurrnBase, CurrnShow
from schemas.user import User
from api.utils.currencies import get_currency, get_symbol, post_symbol_data, get_symbol_data, delete_symbol_data_db
from api.utils.bases import get_function_datalist
from api.utils.oauth2 import get_current_active_user, get_current_active_admin
# from api.utils.utils import symbol_query

tag = "Currency"
router = fastapi.APIRouter(
    prefix="/currency",
    tags=[tag],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CurrnBase])
async def read_currency(
    skip: int = 0, 
    limit: int = 100, 
    db: Session =Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
    ):
    db_currency = get_currency(db, skip=skip, limit=skip+limit)
    if not db_currency:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Currency data not found")
    return db_currency


@router.post("/{function}", status_code=status.HTTP_201_CREATED, response_model=Currn)
async def create_symbol_data(
    base: CurrnCreate, 
    function: Annotated[str, Path(max_length=100)], 
    type: str = Query(enum=[tag]), 
    db: Session = Depends(get_db),
    current_user: User =Depends(get_current_active_admin),
    ):
    result = get_function_datalist(db=db, function=function)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Function not found. Please create the Function before create symbol data.")
    result = get_symbol_data(db=db, function=function, symbol=base.symbol, datetime=base.datetime)
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Symbol data is already existed.")
    return post_symbol_data(db=db, base=base, function=function)


@router.get("/{function}/{symbol}", status_code=status.HTTP_200_OK, response_model=List[CurrnBase])
async def read_symbol(
    symbol: Annotated[str, Path(max_length=50)], 
    function: Annotated[str, Path(max_length=100)], 
    start_date: str | None = None, 
    end_date: str | None = None, 
    db: Session =Depends(get_db), 
    current_user: User =Depends(get_current_active_user)
    ):
    try:
        start_date = parse("1988-01-01").isoformat() if start_date in [None, ""] else parse(start_date).isoformat()
        end_date = datetime.now().isoformat() if end_date in [None, ""] else parse(end_date).isoformat()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.__class__}, {e.__context__}")
    db_symbol = get_symbol(db=db, function=function, symbol=symbol, start_date=start_date, end_date=end_date)
    if not db_symbol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Symbol data not found")
    return db_symbol


@router.delete("/{function}/{symbol}/{datetime}", status_code=status.HTTP_202_ACCEPTED, response_model=CurrnShow)
async def delete_symbol_data(
    function: Annotated[str, Path(max_length=100)], 
    symbol: Annotated[str, Path(max_length=50)],
    datetime: Annotated[datetime, Path()], 
    db: Session =Depends(get_db),
    current_user: User =Depends(get_current_active_admin),
    ):
    db_delete = get_symbol_data(db=db, function=function, symbol=symbol, datetime=datetime)
    if not db_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Symbol data not found")
    return delete_symbol_data_db(db=db, function=function, symbol=symbol, datetime=datetime)


@router.delete("/{function}/{symbol}", status_code=status.HTTP_202_ACCEPTED, response_model=List[CurrnShow])
async def delete_symbol_all_data(
    function: Annotated[str, Path(max_length=100)], 
    symbol: Annotated[str, Path(max_length=50)],
    db: Session =Depends(get_db),
    current_user: User =Depends(get_current_active_admin)
    ):
    db_delete = get_symbol(db=db, function=function, symbol=symbol, start_date=None, end_date=None)
    if not db_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Symbol data not found")
    return delete_symbol_data_db(db=db, function=function, symbol=symbol, datetime=None)