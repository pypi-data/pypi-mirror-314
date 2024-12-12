from typing import Literal, cast

UserMessageRole = Literal["user"]

USER_MESSAGE_ROLE_VALUES: set[UserMessageRole] = {
    "user",
}


def check_user_message_role(value: str) -> UserMessageRole:
    if value in USER_MESSAGE_ROLE_VALUES:
        return cast(UserMessageRole, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {USER_MESSAGE_ROLE_VALUES!r}")
