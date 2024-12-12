from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import TypeVar
from typing import Union

from attrs import define as _attrs_define

from ..models.group_get_group_members_response_200_users import (
    GroupGetGroupMembersResponse200Users,
)
from ..models.group_member import GroupMember
from ..models.pagination import Pagination
from ..types import UNSET
from ..types import Unset


T = TypeVar("T", bound="GroupGetGroupMembersResponse200")


@_attrs_define
class GroupGetGroupMembersResponse200:
    """GroupGetGroupMembersResponse200 model

    Attributes:
        members (List['GroupMember']):
        pagination (Pagination):
        users (Union[Unset, GroupGetGroupMembersResponse200Users]):
    """

    members: List["GroupMember"]
    pagination: "Pagination"
    users: Union[Unset, "GroupGetGroupMembersResponse200Users"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        members = []
        for members_item_data in self.members:
            members_item = members_item_data.to_dict()
            members.append(members_item)

        pagination = self.pagination.to_dict()
        users: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.users, Unset):
            users = self.users.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "members": members,
                "pagination": pagination,
            }
        )
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`GroupGetGroupMembersResponse200` from a dict"""
        d = src_dict.copy()
        members = []
        _members = d.pop("members")
        for members_item_data in _members:
            members_item = GroupMember.from_dict(members_item_data)

            members.append(members_item)

        pagination = Pagination.from_dict(d.pop("pagination"))

        _users = d.pop("users", UNSET)
        users: Union[Unset, GroupGetGroupMembersResponse200Users]
        if isinstance(_users, Unset):
            users = UNSET
        else:
            users = GroupGetGroupMembersResponse200Users.from_dict(_users)

        group_get_group_members_response_200 = cls(
            members=members,
            pagination=pagination,
            users=users,
        )

        return group_get_group_members_response_200
