from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar
from typing import Union

from attrs import define as _attrs_define

from ..models.parser_options_additional_property_type import (
    ParserOptionsAdditionalPropertyType,
)
from ..types import UNSET
from ..types import Unset


T = TypeVar("T", bound="ParserOptionsAdditionalProperty")


@_attrs_define
class ParserOptionsAdditionalProperty:
    """ParserOptionsAdditionalProperty model

    Attributes:
        type (ParserOptionsAdditionalPropertyType):
        allow_null (Union[Unset, bool]):  Default: False.
        default (Union[Unset, Any]):
    """

    type: ParserOptionsAdditionalPropertyType
    allow_null: Union[Unset, bool] = False
    default: Union[Unset, Any] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        type = self.type.value
        allow_null = self.allow_null
        default = self.default

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type,
            }
        )
        if allow_null is not UNSET:
            field_dict["allow_null"] = allow_null
        if default is not UNSET:
            field_dict["default"] = default

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`ParserOptionsAdditionalProperty` from a dict"""
        d = src_dict.copy()
        type = ParserOptionsAdditionalPropertyType(d.pop("type"))

        allow_null = d.pop("allow_null", UNSET)

        default = d.pop("default", UNSET)

        parser_options_additional_property = cls(
            type=type,
            allow_null=allow_null,
            default=default,
        )

        return parser_options_additional_property
