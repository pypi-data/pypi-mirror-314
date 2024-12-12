from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import TypeVar
from typing import Union

from attrs import define as _attrs_define

from ..models.admin_grants import AdminGrants
from ..models.admin_operations_item import AdminOperationsItem
from ..types import UNSET
from ..types import Unset


T = TypeVar("T", bound="AdminList")


@_attrs_define
class AdminList:
    """AdminList model

    Attributes:
        grants (List['AdminGrants']):
        operations (Union[Unset, List[AdminOperationsItem]]):
    """

    grants: List["AdminGrants"]
    operations: Union[Unset, List[AdminOperationsItem]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        grants = []
        for grants_item_data in self.grants:
            grants_item = grants_item_data.to_dict()
            grants.append(grants_item)

        operations: Union[Unset, List[str]] = UNSET
        if not isinstance(self.operations, Unset):
            operations = []
            for componentsschemasadmin_operations_item_data in self.operations:
                componentsschemasadmin_operations_item = (
                    componentsschemasadmin_operations_item_data.value
                )
                operations.append(componentsschemasadmin_operations_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "grants": grants,
            }
        )
        if operations is not UNSET:
            field_dict["operations"] = operations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`AdminList` from a dict"""
        d = src_dict.copy()
        grants = []
        _grants = d.pop("grants")
        for grants_item_data in _grants:
            grants_item = AdminGrants.from_dict(grants_item_data)

            grants.append(grants_item)

        operations = []
        _operations = d.pop("operations", UNSET)
        for componentsschemasadmin_operations_item_data in _operations or []:
            componentsschemasadmin_operations_item = AdminOperationsItem(
                componentsschemasadmin_operations_item_data
            )

            operations.append(componentsschemasadmin_operations_item)

        admin_list = cls(
            grants=grants,
            operations=operations,
        )

        return admin_list
