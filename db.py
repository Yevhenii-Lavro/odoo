from typing import Self, Any, Optional

import mongoengine


class MongoDBConnection:

    __instance: Optional['MongoDBConnection'] = None

    def __new__(cls, *args, **kwargs) -> 'MongoDBConnection':
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, url: str, db_name: str, port: int) -> None:
        self.url = url
        self.db_name = db_name
        self.port = port
        self.connection = None

    async def __aenter__(self) -> Self:
        self.connection = mongoengine.connection.connect(self.db_name, host=self.url, port=self.port)
        return self

    async def __aexit__(self, exc_type: type[Exception], exc: Exception, tb: Any) -> None:
        mongoengine.connection.disconnect(alias=self.db_name)
