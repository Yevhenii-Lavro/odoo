import uuid
from typing import Any
import fastapi

from main.db_models.contacts import Contacts
from main.dependencies.auth import _CheckToken

contact_router = fastapi.APIRouter()


@contact_router.get(
    path='/contact/contact_list',
    dependencies=[
        fastapi.Depends(_CheckToken())
    ],
    summary='get list of the current contacts',
    tags=['contact']
)
async def get_contact_list() -> list[uuid.UUID]:
    return Contacts.objects.all().scalar(Contacts._id.db_field)


@contact_router.get(
    path='/contact/{contact_id}',
    dependencies=[
        fastapi.Depends(_CheckToken())
    ],
    summary='get certain contact by id',
    tags=['contact']
)
async def get_contact(contact_id: uuid.UUID) -> dict[str, Any]:
    return Contacts.objects.get(_id=contact_id).to_mongo()


@contact_router.get(
    path='/contact/external/{contact_external_id}',
    dependencies=[
        fastapi.Depends(_CheckToken())
    ],
    summary='get certain contact by external id',
    tags=['contact']
)
async def get_contact(contact_external_id: int) -> dict[str, Any]:
    return Contacts.objects.get(external_id=contact_external_id).to_mongo()

