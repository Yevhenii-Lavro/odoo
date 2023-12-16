import contextlib
import ssl
import typing
from typing import Final

import urllib.parse
import fastapi
import os

from db import MongoDBConnection
from main.routers.authorization_api import auth_router
from main.routers.contact_api import contact_router
from main.scheduler.scheduler import scheduler

DB_URL: Final[str] = os.getenv('DB_URL', 'mongodb://localhost:27017/')
DB_PORT: Final[int] = int(os.getenv('DB_PORT', 27017))
DB_NAME: Final[str] = os.getenv('DB_NAME', 'TEST')

ODOO_URL: Final[str] = os.getenv('ODOO_URL', 'https://chift.odoo.com')
ODOO_USERNAME: Final[str] = os.getenv('ODOO_USERNAME', 'a.kyrychenko@digiscorp.com')
ODOO_PASSWORD: Final[str] = os.getenv('ODOO_PASSWORD', 'a.kyrychenko@digiscorp.com')
oddo_db: str = urllib.parse.urlparse(url=ODOO_URL).hostname.split('.')[0]

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


@contextlib.asynccontextmanager
async def lifespan(_: fastapi.FastAPI) -> typing.AsyncContextManager[None]:
    async with MongoDBConnection(url=DB_URL, port=DB_PORT, db_name=DB_NAME):
        yield


app = fastapi.FastAPI(lifespan=lifespan)
app.include_router(auth_router, prefix='/api')
app.include_router(contact_router, prefix='/api')

scheduler.start()
