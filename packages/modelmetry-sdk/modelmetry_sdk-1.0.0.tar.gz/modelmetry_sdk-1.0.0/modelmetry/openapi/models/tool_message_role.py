from typing import Literal, cast

ToolMessageRole = Literal["tool"]

TOOL_MESSAGE_ROLE_VALUES: set[ToolMessageRole] = {
    "tool",
}


def check_tool_message_role(value: str) -> ToolMessageRole:
    if value in TOOL_MESSAGE_ROLE_VALUES:
        return cast(ToolMessageRole, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TOOL_MESSAGE_ROLE_VALUES!r}")
