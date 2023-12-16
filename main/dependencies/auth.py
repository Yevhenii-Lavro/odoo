import logging
from typing import Annotated, Any

import fastapi.security

from main.token.token import validate_jwt

logger = logging.getLogger(__name__)


class _CheckToken:
    async def __call__(
        self,
        header_token: Annotated[
            str | None,
            fastapi.Security(
                fastapi.security.APIKeyHeader(name='token', auto_error=False)
            )
        ] = None,
        cookie_token: Annotated[
            str | None,
            fastapi.Security(
                fastapi.security.APIKeyCookie(name='token', auto_error=False)
            )
        ] = None
    ) -> dict[str, Any]:
        token = header_token or cookie_token

        if not token:
            msg = 'User is unauthorized'
            logger.info(msg=msg)
            raise RuntimeError(msg)
        return validate_jwt(token)


UserData = Annotated[dict[str, Any], fastapi.Depends(_CheckToken(), use_cache=False)]
