from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import TypeVar

from attrs import define as _attrs_define

from ..models.group import Group
from ..models.pagination import Pagination


T = TypeVar("T", bound="GroupGetGroupsResponse200")


@_attrs_define
class GroupGetGroupsResponse200:
    """GroupGetGroupsResponse200 model

    Attributes:
        groups (List['Group']):
        pagination (Pagination):
    """

    groups: List["Group"]
    pagination: "Pagination"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        groups = []
        for groups_item_data in self.groups:
            groups_item = groups_item_data.to_dict()
            groups.append(groups_item)

        pagination = self.pagination.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "groups": groups,
                "pagination": pagination,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`GroupGetGroupsResponse200` from a dict"""
        d = src_dict.copy()
        groups = []
        _groups = d.pop("groups")
        for groups_item_data in _groups:
            groups_item = Group.from_dict(groups_item_data)

            groups.append(groups_item)

        pagination = Pagination.from_dict(d.pop("pagination"))

        group_get_groups_response_200 = cls(
            groups=groups,
            pagination=pagination,
        )

        return group_get_groups_response_200
