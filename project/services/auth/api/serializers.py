from typing import Literal

from pydantic import BaseModel


class JWTSerializer(BaseModel):
    """"""

    access_token: str
    refresh_token: str
    token_type: Literal["Bearer"] = "Bearer"
