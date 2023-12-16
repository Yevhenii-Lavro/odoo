import os
from datetime import datetime, timedelta
from typing import TypeAlias, Any, Final

import jwt

Token: TypeAlias = str
TOKEN_SALT: Final[str] = os.getenv('SALT') or 'SALT'


def create_jwt(payload: dict[str, Any]) -> Token:
    payload['exp'] = datetime.utcnow() + timedelta(days=1)
    jwt_token = jwt.encode(payload, TOKEN_SALT, algorithm='HS256')
    return jwt_token


def validate_jwt(token: Token) -> dict[str, Any]:
    try:
        payload = jwt.decode(token.strip('"'), TOKEN_SALT, algorithms=['HS256'])
        del payload['exp']
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token is expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')
