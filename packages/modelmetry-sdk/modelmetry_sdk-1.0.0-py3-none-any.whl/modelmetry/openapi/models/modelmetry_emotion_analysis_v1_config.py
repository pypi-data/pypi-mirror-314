from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ModelmetryEmotionAnalysisV1Config")


@_attrs_define
class ModelmetryEmotionAnalysisV1Config:
    """ """

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        modelmetry_emotion_analysis_v1_config = cls()

        return modelmetry_emotion_analysis_v1_config
