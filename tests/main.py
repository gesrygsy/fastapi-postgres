from fastapi import FastAPI
import uvicorn

from api import bases, currencies, authentications, users, accounts
from db.database import engine
from db.models import base, currency, user, account


base.Base.metadata.create_all(bind=engine)
currency.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)
account.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="FastAPI",
    description="FastAPI + postgres",
    version="0.0.1",
)


app.include_router(authentications.router)
app.include_router(bases.router)
app.include_router(currencies.router)
app.include_router(users.router)
app.include_router(accounts.router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        # reload=True,
    )