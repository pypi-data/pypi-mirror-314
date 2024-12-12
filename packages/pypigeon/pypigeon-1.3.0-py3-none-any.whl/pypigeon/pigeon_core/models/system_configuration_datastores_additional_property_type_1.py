from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import TypeVar
from typing import Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.system_configuration_datastores_additional_property_type_1_type import (
    SystemConfigurationDatastoresAdditionalPropertyType1Type,
)
from ..types import UNSET
from ..types import Unset


T = TypeVar("T", bound="SystemConfigurationDatastoresAdditionalPropertyType1")


@_attrs_define
class SystemConfigurationDatastoresAdditionalPropertyType1:
    """SystemConfigurationDatastoresAdditionalPropertyType1 model

    Attributes:
        bucket (str):
        access_key (Union[Unset, str]):
        cache_max (Union[Unset, int]):  Default: 1073741824.
        enabled (Union[Unset, bool]):  Default: True.
        endpoint_url (Union[Unset, str]):
        is_default (Union[Unset, bool]):  Default: False.
        secret_key (Union[Unset, str]):
        type (Union[Unset, SystemConfigurationDatastoresAdditionalPropertyType1Type]):
    """

    bucket: str
    access_key: Union[Unset, str] = UNSET
    cache_max: Union[Unset, int] = 1073741824
    enabled: Union[Unset, bool] = True
    endpoint_url: Union[Unset, str] = UNSET
    is_default: Union[Unset, bool] = False
    secret_key: Union[Unset, str] = UNSET
    type: Union[Unset, SystemConfigurationDatastoresAdditionalPropertyType1Type] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        bucket = self.bucket
        access_key = self.access_key
        cache_max = self.cache_max
        enabled = self.enabled
        endpoint_url = self.endpoint_url
        is_default = self.is_default
        secret_key = self.secret_key
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bucket": bucket,
            }
        )
        if access_key is not UNSET:
            field_dict["access_key"] = access_key
        if cache_max is not UNSET:
            field_dict["cache_max"] = cache_max
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if endpoint_url is not UNSET:
            field_dict["endpoint_url"] = endpoint_url
        if is_default is not UNSET:
            field_dict["is_default"] = is_default
        if secret_key is not UNSET:
            field_dict["secret_key"] = secret_key
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`SystemConfigurationDatastoresAdditionalPropertyType1` from a dict"""
        d = src_dict.copy()
        bucket = d.pop("bucket")

        access_key = d.pop("access_key", UNSET)

        cache_max = d.pop("cache_max", UNSET)

        enabled = d.pop("enabled", UNSET)

        endpoint_url = d.pop("endpoint_url", UNSET)

        is_default = d.pop("is_default", UNSET)

        secret_key = d.pop("secret_key", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, SystemConfigurationDatastoresAdditionalPropertyType1Type]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = SystemConfigurationDatastoresAdditionalPropertyType1Type(_type)

        system_configuration_datastores_additional_property_type_1 = cls(
            bucket=bucket,
            access_key=access_key,
            cache_max=cache_max,
            enabled=enabled,
            endpoint_url=endpoint_url,
            is_default=is_default,
            secret_key=secret_key,
            type=type,
        )

        system_configuration_datastores_additional_property_type_1.additional_properties = (
            d
        )
        return system_configuration_datastores_additional_property_type_1

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
