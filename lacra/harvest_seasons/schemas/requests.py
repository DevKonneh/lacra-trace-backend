from uuid import UUID

from lacra.common.schemas.base import PaginationRequest
from lacra.db.enums import HarvestSeasonStatus


class HarvestSeasonListRequest(PaginationRequest):
    commodity_id: list[UUID] | None = None
    commodity_group_id: UUID | None = None
    status: HarvestSeasonStatus | None = None
