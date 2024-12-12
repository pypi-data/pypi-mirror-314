from typing import Literal, cast

ModelmetryTextReadabilityV1ConfigScope = Literal["assistant.last", "interaction.last", "last", "user.last"]

MODELMETRY_TEXT_READABILITY_V1_CONFIG_SCOPE_VALUES: set[ModelmetryTextReadabilityV1ConfigScope] = {
    "assistant.last",
    "interaction.last",
    "last",
    "user.last",
}


def check_modelmetry_text_readability_v1_config_scope(value: str) -> ModelmetryTextReadabilityV1ConfigScope:
    if value in MODELMETRY_TEXT_READABILITY_V1_CONFIG_SCOPE_VALUES:
        return cast(ModelmetryTextReadabilityV1ConfigScope, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODELMETRY_TEXT_READABILITY_V1_CONFIG_SCOPE_VALUES!r}"
    )
