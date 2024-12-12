from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.modelmetry_secret_detector_v1_config_custom_patterns import (
        ModelmetrySecretDetectorV1ConfigCustomPatterns,
    )


T = TypeVar("T", bound="ModelmetrySecretDetectorV1Config")


@_attrs_define
class ModelmetrySecretDetectorV1Config:
    """
    Attributes:
        custom_patterns (Union[Unset, ModelmetrySecretDetectorV1ConfigCustomPatterns]): Custom regex patterns to detect
            secrets
    """

    custom_patterns: Union[Unset, "ModelmetrySecretDetectorV1ConfigCustomPatterns"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        custom_patterns: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.custom_patterns, Unset):
            custom_patterns = self.custom_patterns.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if custom_patterns is not UNSET:
            field_dict["CustomPatterns"] = custom_patterns

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.modelmetry_secret_detector_v1_config_custom_patterns import (
            ModelmetrySecretDetectorV1ConfigCustomPatterns,
        )

        d = src_dict.copy()
        _custom_patterns = d.pop("CustomPatterns", UNSET)
        custom_patterns: Union[Unset, ModelmetrySecretDetectorV1ConfigCustomPatterns]
        if isinstance(_custom_patterns, Unset):
            custom_patterns = UNSET
        else:
            custom_patterns = ModelmetrySecretDetectorV1ConfigCustomPatterns.from_dict(_custom_patterns)

        modelmetry_secret_detector_v1_config = cls(
            custom_patterns=custom_patterns,
        )

        return modelmetry_secret_detector_v1_config
