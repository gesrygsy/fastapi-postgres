from typing import List
from datetime import datetime

import fastapi
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.currency import Currn, CurrnCreate, CurrnBase
from schemas.user import User
from api.utils.currencies import get_currency, get_symbol, post_symbol_data, get_symbol_data, delete_symbol_data
from api.utils.oauth2 import get_current_user


router = fastapi.APIRouter(
    prefix="/currency",
    tags=["Currency"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CurrnBase])
async def read_currency(db: Session =Depends(get_db), skip: int = 0, limit: int = 100, current_user: User =Depends(get_current_user)):
    db_currency = get_currency(db, skip=skip, limit=skip+limit)
    if not db_currency:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Currency data not found")
    return db_currency


@router.post("/{symbol}", status_code=status.HTTP_200_OK, response_model=Currn)
async def create_symbol_data(base: CurrnCreate, db: Session = Depends(get_db), current_user: User =Depends(get_current_user)):
    result = get_symbol_data(db=db, symbol=base.symbol, datetime=base.datetime)
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Symbol data is already existed.")
    return post_symbol_data(db=db, base=base)


@router.get("/{symbol}", status_code=status.HTTP_200_OK, response_model=List[CurrnBase])
async def read_symbol(symbol: str, start_date: str | None = None, end_date: str | None = None, db: Session =Depends(get_db), current_user: User =Depends(get_current_user)):
    db_symbol = get_symbol(db=db, symbol=symbol, start_date=start_date, end_date=end_date)
    if not db_symbol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Symbol data not found")
    return db_symbol


@router.delete("/{symbol}/{datetime}", status_code=status.HTTP_200_OK, response_model=Currn)
async def delete_currency_data(symbol: str, datetime: datetime, db: Session =Depends(get_db), current_user: User =Depends(get_current_user)):
    db_delete = get_symbol_data(db=db, symbol=symbol, datetime=datetime)
    if not db_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Symbol data not found")
    return delete_symbol_data(db=db, symbol=symbol, datetime=datetime)


@router.delete("/{symbol}/", status_code=status.HTTP_200_OK, response_model=List[Currn])
async def delete_symbol_all_data(symbol: str, db: Session =Depends(get_db), current_user: User =Depends(get_current_user)):
    db_delete = get_symbol(db=db, symbol=symbol, start_date=None, end_date=None)
    if not db_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Symbol data not found")
    return delete_symbol_data(db=db, symbol=symbol, datetime=None)