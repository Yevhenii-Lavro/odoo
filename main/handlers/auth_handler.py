import contextlib
import uuid

import pydantic
import datetime

from jwt import InvalidTokenError

from main.db_models.users import Users
from main.handlers.odoo_auth_handler import odoo_authorization_uuid
from main.routers.validation_models.authorization_models import TokenGenerationModel
from main.token.password import get_password_hash, verify_password
from main.token.token import create_jwt, Token, validate_jwt


class AuthHandler:

    def __init__(self, *, payload: pydantic.BaseModel) -> None:
        self.payload = payload

    async def sign_up(self) -> uuid.UUID | bool:
        with contextlib.suppress(Exception):
            hashed_password = get_password_hash(self.payload.password)
            odoo_id = await odoo_authorization_uuid()
            data = self.payload.model_dump(mode='json', exclude={'password'})
            data['odoo_id'] = odoo_id
            token = create_jwt(data)
            user = Users(
                name=self.payload.name,
                last_name=self.payload.last_name,
                email=self.payload.email,
                password=hashed_password,
                token=token,
                odoo_id=odoo_id
            )
            user.save()
            return user._id
        return False

    async def login(self) -> Token:
        user = Users.objects(email=self.payload.email).first()
        if not user:
            raise ValueError('email is incorrect')

        res = verify_password(entered_password=self.payload.password, hashed_password=user.password)
        if not res:
            raise ValueError('password is incorrect')

        with contextlib.suppress(InvalidTokenError, ValueError):
            validate_jwt(user.token)
            return user.token

        login_model = TokenGenerationModel(
            name=user.name,
            last_name=user.last_name,
            email=user.email
        )
        odoo_id = await odoo_authorization_uuid()
        login = login_model.model_dump(mode='json')
        login['odoo_id'] = odoo_id
        user.token = create_jwt(login)
        user.save()
        return user.token
