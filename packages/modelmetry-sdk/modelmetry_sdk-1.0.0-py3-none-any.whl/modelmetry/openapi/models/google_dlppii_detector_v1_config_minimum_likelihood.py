from typing import Literal, cast

GoogleDLPPIIDetectorV1ConfigMinimumLikelihood = Literal[
    "LIKELY", "POSSIBLE", "UNLIKELY", "VERY_LIKELY", "VERY_UNLIKELY"
]

GOOGLE_DLPPII_DETECTOR_V1_CONFIG_MINIMUM_LIKELIHOOD_VALUES: set[GoogleDLPPIIDetectorV1ConfigMinimumLikelihood] = {
    "LIKELY",
    "POSSIBLE",
    "UNLIKELY",
    "VERY_LIKELY",
    "VERY_UNLIKELY",
}


def check_google_dlppii_detector_v1_config_minimum_likelihood(
    value: str,
) -> GoogleDLPPIIDetectorV1ConfigMinimumLikelihood:
    if value in GOOGLE_DLPPII_DETECTOR_V1_CONFIG_MINIMUM_LIKELIHOOD_VALUES:
        return cast(GoogleDLPPIIDetectorV1ConfigMinimumLikelihood, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GOOGLE_DLPPII_DETECTOR_V1_CONFIG_MINIMUM_LIKELIHOOD_VALUES!r}"
    )
