import os
from typing import Final

import aioxmlrpc.client
from main.db_models.contacts import Contacts
from main.handlers.odoo_auth_handler import odoo_authorization_uuid
from apscheduler.schedulers.asyncio import AsyncIOScheduler


JOB_TIMER: Final[int] = int(os.getenv('JOB_TIMER', '1'))


async def get_odoo_contact() -> None:
    from app import ssl_context, ODOO_URL, oddo_db, ODOO_PASSWORD
    uid = await odoo_authorization_uuid()
    models = aioxmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object', context=ssl_context)
    res = await models.execute_kw(
        oddo_db,
        uid,
        ODOO_PASSWORD,
        'res.partner',
        'search_read',
        [[['is_company', '=', True]]],
        {'fields': ['name', 'country_id', 'comment']}
    )
    registered_ids = set(Contacts.objects.filter().scalar(Contacts.external_id.db_field))
    for contact in res:
        if contact.get('id') not in registered_ids:
            country_id, country = contact.get('country_id') or [None, None]
            Contacts(
                external_id=contact.get('id'),
                name=contact.get('name'),
                country_id=country_id,
                country=country,
                comment=contact.get('comment')
            ).save()
            break


scheduler = AsyncIOScheduler()
scheduler.add_job(get_odoo_contact, 'interval', minutes=JOB_TIMER)

