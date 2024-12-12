from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ModelmetryLanguageDetectorV1Config")


@_attrs_define
class ModelmetryLanguageDetectorV1Config:
    """
    Attributes:
        confidence_threshold (float): Minimum confidence threshold for the language detection. If the confidence is
            lower than this, the evaluation will be skipped. Default: 0.2.
        word_count_threshold (int): Minimum number of words to check, as the language detection can be unreliable for
            very short texts. Texts shorter than the minimum will be skipped. Default: 2.
    """

    confidence_threshold: float = 0.2
    word_count_threshold: int = 2

    def to_dict(self) -> dict[str, Any]:
        confidence_threshold = self.confidence_threshold

        word_count_threshold = self.word_count_threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "ConfidenceThreshold": confidence_threshold,
                "WordCountThreshold": word_count_threshold,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        confidence_threshold = d.pop("ConfidenceThreshold")

        word_count_threshold = d.pop("WordCountThreshold")

        modelmetry_language_detector_v1_config = cls(
            confidence_threshold=confidence_threshold,
            word_count_threshold=word_count_threshold,
        )

        return modelmetry_language_detector_v1_config
