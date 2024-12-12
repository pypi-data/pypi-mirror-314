from typing import Literal, cast

ModelmetryCompetitorBlocklistV1ConfigLookIn = Literal["*", "assistant", "user"]

MODELMETRY_COMPETITOR_BLOCKLIST_V1_CONFIG_LOOK_IN_VALUES: set[ModelmetryCompetitorBlocklistV1ConfigLookIn] = {
    "*",
    "assistant",
    "user",
}


def check_modelmetry_competitor_blocklist_v1_config_look_in(value: str) -> ModelmetryCompetitorBlocklistV1ConfigLookIn:
    if value in MODELMETRY_COMPETITOR_BLOCKLIST_V1_CONFIG_LOOK_IN_VALUES:
        return cast(ModelmetryCompetitorBlocklistV1ConfigLookIn, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODELMETRY_COMPETITOR_BLOCKLIST_V1_CONFIG_LOOK_IN_VALUES!r}"
    )
