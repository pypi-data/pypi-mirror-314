from typing import Literal, cast

AssistantMessageRole = Literal["assistant"]

ASSISTANT_MESSAGE_ROLE_VALUES: set[AssistantMessageRole] = {
    "assistant",
}


def check_assistant_message_role(value: str) -> AssistantMessageRole:
    if value in ASSISTANT_MESSAGE_ROLE_VALUES:
        return cast(AssistantMessageRole, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ASSISTANT_MESSAGE_ROLE_VALUES!r}")
