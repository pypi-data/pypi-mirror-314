from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelmetryJSONValidatorV1Config")


@_attrs_define
class ModelmetryJSONValidatorV1Config:
    """
    Attributes:
        expected_json_schema (Union[Unset, str]): The expected JSON schema to validate against
    """

    expected_json_schema: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        expected_json_schema = self.expected_json_schema

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if expected_json_schema is not UNSET:
            field_dict["ExpectedJSONSchema"] = expected_json_schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        expected_json_schema = d.pop("ExpectedJSONSchema", UNSET)

        modelmetry_json_validator_v1_config = cls(
            expected_json_schema=expected_json_schema,
        )

        return modelmetry_json_validator_v1_config
