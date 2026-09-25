from dataclasses import dataclass

from lacra.db.enums import GadgetType
from lacra.db.models import Gadget
from lacra.users.schemas.dto import GadgetDTO


@dataclass(slots=True)
class GadgetsMapper:
    @staticmethod
    def to_dto(entity: Gadget) -> GadgetDTO:
        return GadgetDTO(
            id=entity.id,
            type=GadgetType(entity.type),
            identifier=entity.identifier,
            is_verified=entity.is_verified,
        )

    @staticmethod
    def to_dto_list(entities: list[Gadget]) -> list[GadgetDTO]:
        return [GadgetsMapper.to_dto(entity) for entity in entities]
