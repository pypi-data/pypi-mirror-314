from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar
from typing import Union

from attrs import define as _attrs_define

from ..models.item_parser_options import ItemParserOptions
from ..types import UNSET
from ..types import Unset


T = TypeVar("T", bound="ItemParser")


@_attrs_define
class ItemParser:
    """ItemParser model

    Example:

    >>> model = ItemParser.from_dict({'name': 'auto'})

    Attributes:
        name (str):
        options (Union[Unset, ItemParserOptions]):
    """

    name: str
    options: Union[Unset, "ItemParserOptions"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        name = self.name
        options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`ItemParser` from a dict"""
        d = src_dict.copy()
        name = d.pop("name")

        _options = d.pop("options", UNSET)
        options: Union[Unset, ItemParserOptions]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = ItemParserOptions.from_dict(_options)

        item_parser = cls(
            name=name,
            options=options,
        )

        return item_parser
