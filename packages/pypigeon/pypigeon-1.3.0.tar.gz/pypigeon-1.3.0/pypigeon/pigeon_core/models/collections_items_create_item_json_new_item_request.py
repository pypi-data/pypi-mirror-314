from typing import Any
from typing import cast
from typing import Dict
from typing import List
from typing import Type
from typing import TypeVar
from typing import Union

from attrs import define as _attrs_define

from ..models.collections_items_create_item_json_new_item_request_content import (
    CollectionsItemsCreateItemJsonNewItemRequestContent,
)
from ..models.item_column import ItemColumn
from ..models.item_metadata import ItemMetadata
from ..models.item_parser import ItemParser
from ..models.item_storage import ItemStorage
from ..models.item_type import ItemType
from ..types import UNSET
from ..types import Unset


T = TypeVar("T", bound="CollectionsItemsCreateItemJsonNewItemRequest")


@_attrs_define
class CollectionsItemsCreateItemJsonNewItemRequest:
    """CollectionsItemsCreateItemJsonNewItemRequest model

    Attributes:
        name (str): Item name
        type (ItemType):
        columns (Union[List['ItemColumn'], None, Unset]):
        content (Union[Unset, CollectionsItemsCreateItemJsonNewItemRequestContent]): If uploading a small file, the
            contents can be provided.
        folder_id (Union[Unset, str]): Item ID of parent folder, or ROOT Example: ROOT.
        metadata (Union[Unset, ItemMetadata]): Arbitrary metadata as key-value string pairs
        parser (Union['ItemParser', None, Unset]):  Example: {'name': 'auto'}.
        storage (Union['ItemStorage', None, Unset]):  Example: {'checksum': {}, 'size': None, 'sizeIsEstimate': False,
            'url': 'pigeon+datastore://default'}.
    """

    name: str
    type: ItemType
    columns: Union[List["ItemColumn"], None, Unset] = UNSET
    content: Union[Unset, "CollectionsItemsCreateItemJsonNewItemRequestContent"] = UNSET
    folder_id: Union[Unset, str] = UNSET
    metadata: Union[Unset, "ItemMetadata"] = UNSET
    parser: Union["ItemParser", None, Unset] = UNSET
    storage: Union["ItemStorage", None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        name = self.name
        type = self.type.value
        columns: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.columns, Unset):
            columns = UNSET
        elif isinstance(self.columns, list):
            columns = []
            for componentsschemasitem_columns_type_0_item_data in self.columns:
                componentsschemasitem_columns_type_0_item = (
                    componentsschemasitem_columns_type_0_item_data.to_dict()
                )
                columns.append(componentsschemasitem_columns_type_0_item)

        else:
            columns = self.columns
        content: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.content, Unset):
            content = self.content.to_dict()
        folder_id = self.folder_id
        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()
        parser: Union[Dict[str, Any], None, Unset]
        if isinstance(self.parser, Unset):
            parser = UNSET
        elif isinstance(self.parser, ItemParser):
            parser = self.parser.to_dict()
        else:
            parser = self.parser
        storage: Union[Dict[str, Any], None, Unset]
        if isinstance(self.storage, Unset):
            storage = UNSET
        elif isinstance(self.storage, ItemStorage):
            storage = self.storage.to_dict()
        else:
            storage = self.storage

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "type": type,
            }
        )
        if columns is not UNSET:
            field_dict["columns"] = columns
        if content is not UNSET:
            field_dict["content"] = content
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if parser is not UNSET:
            field_dict["parser"] = parser
        if storage is not UNSET:
            field_dict["storage"] = storage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`CollectionsItemsCreateItemJsonNewItemRequest` from a dict"""
        d = src_dict.copy()
        name = d.pop("name")

        type = ItemType(d.pop("type"))

        def _parse_columns(data: object) -> Union[List["ItemColumn"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemasitem_columns_type_0 = []
                _componentsschemasitem_columns_type_0 = data
                for (
                    componentsschemasitem_columns_type_0_item_data
                ) in _componentsschemasitem_columns_type_0:
                    componentsschemasitem_columns_type_0_item = ItemColumn.from_dict(
                        componentsschemasitem_columns_type_0_item_data
                    )

                    componentsschemasitem_columns_type_0.append(
                        componentsschemasitem_columns_type_0_item
                    )

                return componentsschemasitem_columns_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ItemColumn"], None, Unset], data)

        columns = _parse_columns(d.pop("columns", UNSET))

        _content = d.pop("content", UNSET)
        content: Union[Unset, CollectionsItemsCreateItemJsonNewItemRequestContent]
        if isinstance(_content, Unset):
            content = UNSET
        else:
            content = CollectionsItemsCreateItemJsonNewItemRequestContent.from_dict(
                _content
            )

        folder_id = d.pop("folderId", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, ItemMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ItemMetadata.from_dict(_metadata)

        def _parse_parser(data: object) -> Union["ItemParser", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasitem_parser_type_0 = ItemParser.from_dict(data)

                return componentsschemasitem_parser_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ItemParser", None, Unset], data)

        parser = _parse_parser(d.pop("parser", UNSET))

        def _parse_storage(data: object) -> Union["ItemStorage", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasitem_storage_type_0 = ItemStorage.from_dict(data)

                return componentsschemasitem_storage_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ItemStorage", None, Unset], data)

        storage = _parse_storage(d.pop("storage", UNSET))

        collections_items_create_item_json_new_item_request = cls(
            name=name,
            type=type,
            columns=columns,
            content=content,
            folder_id=folder_id,
            metadata=metadata,
            parser=parser,
            storage=storage,
        )

        return collections_items_create_item_json_new_item_request
