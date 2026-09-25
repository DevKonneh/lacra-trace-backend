from pydantic import BaseModel

from lacra.common.schemas.dto import BaseModelDTO
from lacra.db.enums import GadgetType


class GadgetDTO(BaseModelDTO):
    type: GadgetType
    identifier: str
    is_verified: bool


class UserDTO(BaseModelDTO):
    username: str
    gadgets: list[GadgetDTO]


class GadgetExistsDTO(BaseModel):
    exists: bool
