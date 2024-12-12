from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.modelmetry_competitor_blocklist_v1_config_case_sensitivity import (
    ModelmetryCompetitorBlocklistV1ConfigCaseSensitivity,
    check_modelmetry_competitor_blocklist_v1_config_case_sensitivity,
)
from ..models.modelmetry_competitor_blocklist_v1_config_look_in import (
    ModelmetryCompetitorBlocklistV1ConfigLookIn,
    check_modelmetry_competitor_blocklist_v1_config_look_in,
)

T = TypeVar("T", bound="ModelmetryCompetitorBlocklistV1Config")


@_attrs_define
class ModelmetryCompetitorBlocklistV1Config:
    """
    Attributes:
        case_sensitivity (ModelmetryCompetitorBlocklistV1ConfigCaseSensitivity): Whether to consider the word's case
            when matching strings Default: 'case_sensitive'.
        competitors (Union[None, list[str]]): List of competitors to search for
        look_in (ModelmetryCompetitorBlocklistV1ConfigLookIn): Where to search for competitor mentions Default: '*'.
    """

    competitors: Union[None, list[str]]
    case_sensitivity: ModelmetryCompetitorBlocklistV1ConfigCaseSensitivity = "case_sensitive"
    look_in: ModelmetryCompetitorBlocklistV1ConfigLookIn = "*"

    def to_dict(self) -> dict[str, Any]:
        case_sensitivity: str = self.case_sensitivity

        competitors: Union[None, list[str]]
        if isinstance(self.competitors, list):
            competitors = self.competitors

        else:
            competitors = self.competitors

        look_in: str = self.look_in

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "CaseSensitivity": case_sensitivity,
                "Competitors": competitors,
                "LookIn": look_in,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        case_sensitivity = check_modelmetry_competitor_blocklist_v1_config_case_sensitivity(d.pop("CaseSensitivity"))

        def _parse_competitors(data: object) -> Union[None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                competitors_type_0 = cast(list[str], data)

                return competitors_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str]], data)

        competitors = _parse_competitors(d.pop("Competitors"))

        look_in = check_modelmetry_competitor_blocklist_v1_config_look_in(d.pop("LookIn"))

        modelmetry_competitor_blocklist_v1_config = cls(
            case_sensitivity=case_sensitivity,
            competitors=competitors,
            look_in=look_in,
        )

        return modelmetry_competitor_blocklist_v1_config
