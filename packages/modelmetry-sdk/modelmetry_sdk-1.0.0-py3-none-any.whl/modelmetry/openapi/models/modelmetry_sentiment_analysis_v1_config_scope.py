from typing import Literal, cast

ModelmetrySentimentAnalysisV1ConfigScope = Literal["assistant.last", "interaction.last", "last", "user.last"]

MODELMETRY_SENTIMENT_ANALYSIS_V1_CONFIG_SCOPE_VALUES: set[ModelmetrySentimentAnalysisV1ConfigScope] = {
    "assistant.last",
    "interaction.last",
    "last",
    "user.last",
}


def check_modelmetry_sentiment_analysis_v1_config_scope(value: str) -> ModelmetrySentimentAnalysisV1ConfigScope:
    if value in MODELMETRY_SENTIMENT_ANALYSIS_V1_CONFIG_SCOPE_VALUES:
        return cast(ModelmetrySentimentAnalysisV1ConfigScope, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODELMETRY_SENTIMENT_ANALYSIS_V1_CONFIG_SCOPE_VALUES!r}"
    )
