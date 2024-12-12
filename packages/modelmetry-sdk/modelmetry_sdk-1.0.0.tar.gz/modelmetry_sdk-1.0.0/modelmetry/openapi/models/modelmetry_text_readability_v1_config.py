from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.modelmetry_text_readability_v1_config_scope import (
    ModelmetryTextReadabilityV1ConfigScope,
    check_modelmetry_text_readability_v1_config_scope,
)

T = TypeVar("T", bound="ModelmetryTextReadabilityV1Config")


@_attrs_define
class ModelmetryTextReadabilityV1Config:
    """
    Attributes:
        scope (ModelmetryTextReadabilityV1ConfigScope):  Default: 'last'.
    """

    scope: ModelmetryTextReadabilityV1ConfigScope = "last"

    def to_dict(self) -> dict[str, Any]:
        scope: str = self.scope

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Scope": scope,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        scope = check_modelmetry_text_readability_v1_config_scope(d.pop("Scope"))

        modelmetry_text_readability_v1_config = cls(
            scope=scope,
        )

        return modelmetry_text_readability_v1_config
