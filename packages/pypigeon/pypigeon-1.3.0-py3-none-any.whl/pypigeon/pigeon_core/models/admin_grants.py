from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import TypeVar

from attrs import define as _attrs_define

from ..models.admin_operations_item import AdminOperationsItem


T = TypeVar("T", bound="AdminGrants")


@_attrs_define
class AdminGrants:
    """AdminGrants model

    Attributes:
        operations (List[AdminOperationsItem]):
        subject_id (str):
    """

    operations: List[AdminOperationsItem]
    subject_id: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        operations = []
        for componentsschemasadmin_operations_item_data in self.operations:
            componentsschemasadmin_operations_item = (
                componentsschemasadmin_operations_item_data.value
            )
            operations.append(componentsschemasadmin_operations_item)

        subject_id = self.subject_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "operations": operations,
                "subject_id": subject_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`AdminGrants` from a dict"""
        d = src_dict.copy()
        operations = []
        _operations = d.pop("operations")
        for componentsschemasadmin_operations_item_data in _operations:
            componentsschemasadmin_operations_item = AdminOperationsItem(
                componentsschemasadmin_operations_item_data
            )

            operations.append(componentsschemasadmin_operations_item)

        subject_id = d.pop("subject_id")

        admin_grants = cls(
            operations=operations,
            subject_id=subject_id,
        )

        return admin_grants
