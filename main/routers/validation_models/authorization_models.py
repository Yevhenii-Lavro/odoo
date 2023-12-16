from typing import Annotated

import pydantic


class TokenGenerationModel(pydantic.BaseModel):
    name: str
    last_name: str
    email: str


class PostSignUpBody(TokenGenerationModel):
    password: Annotated[
        str,
        pydantic.StringConstraints(min_length=8, strict=True)
    ]


class PostLoginBody(pydantic.BaseModel):
    password: str
    email: str
