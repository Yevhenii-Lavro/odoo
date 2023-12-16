import aioxmlrpc.client


async def odoo_authorization_uuid() -> int:
    from app import ssl_context, ODOO_URL, oddo_db, ODOO_USERNAME, ODOO_PASSWORD
    common = aioxmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common', context=ssl_context)

    return await common.authenticate(oddo_db, ODOO_USERNAME, ODOO_PASSWORD, {})
