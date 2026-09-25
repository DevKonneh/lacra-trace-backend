from dataclasses import dataclass

from lacra.db.enums import GadgetType
from lacra.db.models import Gadget, User


@dataclass(slots=True)
class UsersStorage:
    @staticmethod
    def get_user_by_gadget(gadget_type: GadgetType, identifier: str) -> User | None:
        try:
            gadget = Gadget.objects.get(type=gadget_type, identifier=identifier)
            return gadget.user
        except Gadget.DoesNotExist:
            return None
