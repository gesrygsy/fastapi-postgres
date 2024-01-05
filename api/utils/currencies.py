from datetime import datetime
from sqlalchemy.orm import Session

from db.models.currency import Currn
from schemas.currency import CurrnCreate



def get_currency(db: Session, skip: int, limit: int, dataset_function="FX"):
    return db.query(Currn).filter(Currn.dataset_function == dataset_function).order_by(Currn.datetime).all()[skip:limit]


def get_symbol(db: Session, symbol: str, start_date: str | None, end_date: str | None):
    if start_date is None:
        start_date = "1988-01-01"
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    start = datetime.strptime(start_date, '%Y-%m-%d').isoformat()
    end = datetime.strptime(end_date, '%Y-%m-%d').isoformat()
    return db.query(Currn).filter(Currn.symbol == symbol).filter(Currn.datetime >= start).filter(Currn.datetime <= end).order_by(Currn.datetime).all()


def post_symbol_data(db: Session, base: CurrnCreate):
    db_symbol = Currn(
        dataset_function="FX",
        symbol=base.symbol,
        datetime=base.datetime,
        open=base.open,
        high=base.high,
        low=base.low,
        close=base.close,
        volume=base.volume,
    )
    db.add(db_symbol)
    db.commit()
    db.refresh(db_symbol)
    return db_symbol


def get_symbol_data(db: Session, symbol: str, datetime: datetime):
    return db.query(Currn).filter((Currn.symbol == symbol) & (Currn.datetime == datetime)).first()


def delete_symbol_data(db: Session, symbol: str, datetime: datetime | None):
    if datetime is None:
        result = db.query(Currn).filter(Currn.symbol == symbol).all()
        for r in result:
            db.delete(r)
    else:
        result = db.query(Currn).filter((Currn.symbol == symbol) & (Currn.datetime == datetime)).first()
        db.delete(result)
    db.commit()
    return result
