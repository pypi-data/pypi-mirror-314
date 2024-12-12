from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.assistant_message import AssistantMessage
    from ..models.completion_payload_options import CompletionPayloadOptions
    from ..models.system_message import SystemMessage
    from ..models.tool_message import ToolMessage
    from ..models.user_message import UserMessage


T = TypeVar("T", bound="CompletionPayload")


@_attrs_define
class CompletionPayload:
    """
    Attributes:
        messages (list[Union['AssistantMessage', 'SystemMessage', 'ToolMessage', 'UserMessage']]):
        options (Union[Unset, CompletionPayloadOptions]):
    """

    messages: list[Union["AssistantMessage", "SystemMessage", "ToolMessage", "UserMessage"]]
    options: Union[Unset, "CompletionPayloadOptions"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.assistant_message import AssistantMessage
        from ..models.system_message import SystemMessage
        from ..models.user_message import UserMessage

        messages = []
        for messages_item_data in self.messages:
            messages_item: dict[str, Any]
            if isinstance(messages_item_data, SystemMessage):
                messages_item = messages_item_data.to_dict()
            elif isinstance(messages_item_data, UserMessage):
                messages_item = messages_item_data.to_dict()
            elif isinstance(messages_item_data, AssistantMessage):
                messages_item = messages_item_data.to_dict()
            else:
                messages_item = messages_item_data.to_dict()

            messages.append(messages_item)

        options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Messages": messages,
            }
        )
        if options is not UNSET:
            field_dict["Options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.assistant_message import AssistantMessage
        from ..models.completion_payload_options import CompletionPayloadOptions
        from ..models.system_message import SystemMessage
        from ..models.tool_message import ToolMessage
        from ..models.user_message import UserMessage

        d = src_dict.copy()
        messages = []
        _messages = d.pop("Messages")
        for messages_item_data in _messages:

            def _parse_messages_item(
                data: object,
            ) -> Union["AssistantMessage", "SystemMessage", "ToolMessage", "UserMessage"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    messages_item_type_0 = SystemMessage.from_dict(data)

                    return messages_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    messages_item_type_1 = UserMessage.from_dict(data)

                    return messages_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    messages_item_type_2 = AssistantMessage.from_dict(data)

                    return messages_item_type_2
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                messages_item_type_3 = ToolMessage.from_dict(data)

                return messages_item_type_3

            messages_item = _parse_messages_item(messages_item_data)

            messages.append(messages_item)

        _options = d.pop("Options", UNSET)
        options: Union[Unset, CompletionPayloadOptions]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = CompletionPayloadOptions.from_dict(_options)

        completion_payload = cls(
            messages=messages,
            options=options,
        )

        return completion_payload
