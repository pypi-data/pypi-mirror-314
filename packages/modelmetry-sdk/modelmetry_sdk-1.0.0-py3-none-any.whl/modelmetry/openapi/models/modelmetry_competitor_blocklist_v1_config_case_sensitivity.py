from typing import Literal, cast

ModelmetryCompetitorBlocklistV1ConfigCaseSensitivity = Literal["case_insensitive", "case_sensitive"]

MODELMETRY_COMPETITOR_BLOCKLIST_V1_CONFIG_CASE_SENSITIVITY_VALUES: set[
    ModelmetryCompetitorBlocklistV1ConfigCaseSensitivity
] = {
    "case_insensitive",
    "case_sensitive",
}


def check_modelmetry_competitor_blocklist_v1_config_case_sensitivity(
    value: str,
) -> ModelmetryCompetitorBlocklistV1ConfigCaseSensitivity:
    if value in MODELMETRY_COMPETITOR_BLOCKLIST_V1_CONFIG_CASE_SENSITIVITY_VALUES:
        return cast(ModelmetryCompetitorBlocklistV1ConfigCaseSensitivity, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODELMETRY_COMPETITOR_BLOCKLIST_V1_CONFIG_CASE_SENSITIVITY_VALUES!r}"
    )
