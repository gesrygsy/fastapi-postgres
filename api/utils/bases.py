from datetime import datetime
from sqlalchemy.orm import Session

from db.models.base import Dataset


def get_function_datalist(db: Session, function: str):
    return db.query(Dataset).filter(Dataset.function == function).first()


def get_type_datalist(db: Session, type: str):
    return db.query(Dataset).filter(Dataset.type == type).all()


def get_all_datalist(db: Session):
    return db.query(Dataset).all()


def create_datalist(db: Session, function: str, type: int, description: str, data_source: str):
    db_datalist = Dataset(
        function=function,
        type=type,
        description=description,
        data_source=data_source,
    )
    db.add(db_datalist)
    db.commit()
    db.refresh(db_datalist)
    return db_datalist


def update_datalist(db: Session, type: str, description: str, data_source: str, to_be_update):
    update = to_be_update
    update.type = type
    update.description = description
    update.data_source = data_source
    update.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(update)
    return update


def delete_datalist(db: Session, function: str):
    result = db.query(Dataset).filter(Dataset.function == function).first()
    db.delete(result)
    db.commit()
    return result