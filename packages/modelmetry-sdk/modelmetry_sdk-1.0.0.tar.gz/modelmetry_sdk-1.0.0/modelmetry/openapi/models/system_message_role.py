from typing import Literal, cast

SystemMessageRole = Literal["system"]

SYSTEM_MESSAGE_ROLE_VALUES: set[SystemMessageRole] = {
    "system",
}


def check_system_message_role(value: str) -> SystemMessageRole:
    if value in SYSTEM_MESSAGE_ROLE_VALUES:
        return cast(SystemMessageRole, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SYSTEM_MESSAGE_ROLE_VALUES!r}")
