from sqlalchemy.orm import Session

from db.models.base import Dataset
from schemas.base import DatasetCreate


def get_function_datalist(db: Session, function: str):
    return db.query(Dataset).filter(Dataset.function == function).first()


def get_all_datalist(db: Session):
    return db.query(Dataset).all()


def create_datalist(db: Session, base: DatasetCreate):
    db_datalist = Dataset(
        function=base.function,
        type=base.type,
        description=base.description,
        data_source=base.data_source,
    )
    db.add(db_datalist)
    db.commit()
    db.refresh(db_datalist)
    return db_datalist


def update_datalist(db: Session, base: DatasetCreate):
    update = db.query(Dataset).filter(Dataset.function == base.function).first()
    update.function = base.function
    update.type = base.type
    update.description = base.description
    update.data_source = base.data_source

    db.commit()
    db.refresh(update)
    return update


def delete_datalist(db: Session, function: str):
    result = db.query(Dataset).filter(Dataset.function == function).first()
    db.delete(result)
    db.commit()
    return result