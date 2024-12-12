from typing import Literal, cast

GoogleTextModerationV1ConfigAttributesType0Item = Literal[
    "DEROGATORY",
    "FINANCIAL",
    "HEALTH",
    "ILLICIT_DRUGS",
    "INSULT",
    "LEGAL",
    "POLITICAL",
    "PROFANITY",
    "PUBLIC_SAFETY",
    "RELIGION",
    "SEX",
    "THREAT",
    "TOXICITY",
    "VIOLENCE",
    "WAR",
    "WEAPONS",
]

GOOGLE_TEXT_MODERATION_V1_CONFIG_ATTRIBUTES_TYPE_0_ITEM_VALUES: set[GoogleTextModerationV1ConfigAttributesType0Item] = {
    "DEROGATORY",
    "FINANCIAL",
    "HEALTH",
    "ILLICIT_DRUGS",
    "INSULT",
    "LEGAL",
    "POLITICAL",
    "PROFANITY",
    "PUBLIC_SAFETY",
    "RELIGION",
    "SEX",
    "THREAT",
    "TOXICITY",
    "VIOLENCE",
    "WAR",
    "WEAPONS",
}


def check_google_text_moderation_v1_config_attributes_type_0_item(
    value: str,
) -> GoogleTextModerationV1ConfigAttributesType0Item:
    if value in GOOGLE_TEXT_MODERATION_V1_CONFIG_ATTRIBUTES_TYPE_0_ITEM_VALUES:
        return cast(GoogleTextModerationV1ConfigAttributesType0Item, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GOOGLE_TEXT_MODERATION_V1_CONFIG_ATTRIBUTES_TYPE_0_ITEM_VALUES!r}"
    )
