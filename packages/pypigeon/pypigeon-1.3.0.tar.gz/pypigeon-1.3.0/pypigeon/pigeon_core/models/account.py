import datetime
from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar
from typing import Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET
from ..types import Unset


T = TypeVar("T", bound="Account")


@_attrs_define
class Account:
    """Account model

    Attributes:
        created_on (datetime.datetime):
        id (str):
        is_personal (bool):
        name (str):
        members_group_id (Union[Unset, str]):
    """

    created_on: datetime.datetime
    id: str
    is_personal: bool
    name: str
    members_group_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        created_on = self.created_on.isoformat()
        id = self.id
        is_personal = self.is_personal
        name = self.name
        members_group_id = self.members_group_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "createdOn": created_on,
                "id": id,
                "isPersonal": is_personal,
                "name": name,
            }
        )
        if members_group_id is not UNSET:
            field_dict["membersGroupId"] = members_group_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`Account` from a dict"""
        d = src_dict.copy()
        created_on = isoparse(d.pop("createdOn"))

        id = d.pop("id")

        is_personal = d.pop("isPersonal")

        name = d.pop("name")

        members_group_id = d.pop("membersGroupId", UNSET)

        account = cls(
            created_on=created_on,
            id=id,
            is_personal=is_personal,
            name=name,
            members_group_id=members_group_id,
        )

        return account
