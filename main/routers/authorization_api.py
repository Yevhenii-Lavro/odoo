import uuid

import fastapi

from main.handlers.auth_handler import AuthHandler as Auth
from main.token.token import Token
from main.routers.validation_models.authorization_models import PostSignUpBody, PostLoginBody

auth_router = fastapi.APIRouter()


@auth_router.post(
    path='/sign-up',
    response_model=None
)
async def sign_up(payload: PostSignUpBody) -> uuid.UUID | bool:
    """
    Sign up (create new user)
    :params in  payload is :
    name: str
    last_name: str
    email: str
    password: str
    :return: bool if sign up failed
    """
    auth = Auth(payload=payload)
    return await auth.sign_up()


@auth_router.post(
    path='/login',
    response_model=None
)
async def login(payload: PostLoginBody) -> Token:
    """
    Login into the system
    :param payload: should include email + password to accept
    :return: str
    """
    auth = Auth(payload=payload)
    return await auth.login()

