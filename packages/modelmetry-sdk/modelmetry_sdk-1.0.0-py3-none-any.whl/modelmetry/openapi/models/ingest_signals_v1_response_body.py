from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="IngestSignalsV1ResponseBody")


@_attrs_define
class IngestSignalsV1ResponseBody:
    """
    Attributes:
        schema (Union[Unset, str]): A URL to the JSON Schema for this object.
    """

    schema: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        schema = d.pop("$schema", UNSET)

        ingest_signals_v1_response_body = cls(
            schema=schema,
        )

        return ingest_signals_v1_response_body
