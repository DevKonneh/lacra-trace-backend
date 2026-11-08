from datetime import date

from lacra.common.schemas.dto import BaseModelDTO
from lacra.db.enums import HarvestSeasonStatus


class HarvestSeasonDTO(BaseModelDTO):
    name: str
    start_date: date
    end_date: date
    status: HarvestSeasonStatus
