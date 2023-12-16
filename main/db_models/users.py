import datetime
import uuid

import mongoengine


class Users(mongoengine.Document):
    _id = mongoengine.UUIDField(default=uuid.uuid4, binary=False)
    name = mongoengine.StringField(required=True)
    last_name = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True, unique=True)
    password = mongoengine.StringField(required=True)
    token = mongoengine.StringField(required=True)
    odoo_id = mongoengine.IntField(required=False)
    date_modified = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
