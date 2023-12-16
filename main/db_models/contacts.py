import uuid

import mongoengine


class Contacts(mongoengine.Document):
    _id = mongoengine.UUIDField(default=uuid.uuid4, binary=False)
    external_id = mongoengine.IntField()
    name = mongoengine.StringField(null=True)
    comment = mongoengine.BooleanField(null=True)
    country = mongoengine.StringField()
    country_id = mongoengine.IntField()
