from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.google_dlppii_detector_v1_config_minimum_likelihood import (
    GoogleDLPPIIDetectorV1ConfigMinimumLikelihood,
    check_google_dlppii_detector_v1_config_minimum_likelihood,
)

T = TypeVar("T", bound="GoogleDLPPIIDetectorV1Config")


@_attrs_define
class GoogleDLPPIIDetectorV1Config:
    """
    Attributes:
        info_types (Union[None, list[str]]): Info types to detect as per Google Cloud DLP's documentation
        minimum_likelihood (GoogleDLPPIIDetectorV1ConfigMinimumLikelihood): Threshold for detection Default: 'LIKELY'.
    """

    info_types: Union[None, list[str]]
    minimum_likelihood: GoogleDLPPIIDetectorV1ConfigMinimumLikelihood = "LIKELY"

    def to_dict(self) -> dict[str, Any]:
        info_types: Union[None, list[str]]
        if isinstance(self.info_types, list):
            info_types = self.info_types

        else:
            info_types = self.info_types

        minimum_likelihood: str = self.minimum_likelihood

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "InfoTypes": info_types,
                "MinimumLikelihood": minimum_likelihood,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_info_types(data: object) -> Union[None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                info_types_type_0 = cast(list[str], data)

                return info_types_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str]], data)

        info_types = _parse_info_types(d.pop("InfoTypes"))

        minimum_likelihood = check_google_dlppii_detector_v1_config_minimum_likelihood(d.pop("MinimumLikelihood"))

        google_dlppii_detector_v1_config = cls(
            info_types=info_types,
            minimum_likelihood=minimum_likelihood,
        )

        return google_dlppii_detector_v1_config
