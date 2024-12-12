from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ModelmetryHTTPRequestV1ConfigHeaders")


@_attrs_define
class ModelmetryHTTPRequestV1ConfigHeaders:
    """A map of headers to include in the request."""

    additional_properties: dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        modelmetry_http_request_v1_config_headers = cls()

        modelmetry_http_request_v1_config_headers.additional_properties = d
        return modelmetry_http_request_v1_config_headers

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
