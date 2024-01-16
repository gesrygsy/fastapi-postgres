from fastapi import FastAPI
import uvicorn

from api import bases, currencies, authentications, users
from db.database import engine
from db.models import base, currency, user


base.Base.metadata.create_all(bind=engine)
currency.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SHIRO's Database",
    description="Financial markets database for personal use.",
    version="0.0.1",
    license_info={
        "name": "MIT",
    }
)


app.include_router(authentications.router)
app.include_router(bases.router)
app.include_router(currencies.router)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
#        ssl_keyfile="/etc/nginx/ssl/server.key",
#        ssl_certfile="/etc/nginx/ssl/server.crt",
    )