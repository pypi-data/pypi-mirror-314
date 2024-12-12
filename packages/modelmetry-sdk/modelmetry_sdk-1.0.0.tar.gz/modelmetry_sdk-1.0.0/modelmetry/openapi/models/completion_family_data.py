from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.assistant_message import AssistantMessage
    from ..models.cost import Cost
    from ..models.document import Document
    from ..models.options import Options
    from ..models.system_message import SystemMessage
    from ..models.tool_message import ToolMessage
    from ..models.usage import Usage
    from ..models.user_message import UserMessage


T = TypeVar("T", bound="CompletionFamilyData")


@_attrs_define
class CompletionFamilyData:
    """
    Attributes:
        cost (Union[Unset, Cost]):
        documents (Union[Unset, list['Document']]):
        messages (Union[Unset, list[Union['AssistantMessage', 'SystemMessage', 'ToolMessage', 'UserMessage']]]):
        options (Union[Unset, Options]):
        usage (Union[Unset, Usage]):
    """

    cost: Union[Unset, "Cost"] = UNSET
    documents: Union[Unset, list["Document"]] = UNSET
    messages: Union[Unset, list[Union["AssistantMessage", "SystemMessage", "ToolMessage", "UserMessage"]]] = UNSET
    options: Union[Unset, "Options"] = UNSET
    usage: Union[Unset, "Usage"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.assistant_message import AssistantMessage
        from ..models.system_message import SystemMessage
        from ..models.user_message import UserMessage

        cost: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cost, Unset):
            cost = self.cost.to_dict()

        documents: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.documents, Unset):
            documents = []
            for documents_item_data in self.documents:
                documents_item = documents_item_data.to_dict()
                documents.append(documents_item)

        messages: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.messages, Unset):
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

        usage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if cost is not UNSET:
            field_dict["Cost"] = cost
        if documents is not UNSET:
            field_dict["Documents"] = documents
        if messages is not UNSET:
            field_dict["Messages"] = messages
        if options is not UNSET:
            field_dict["Options"] = options
        if usage is not UNSET:
            field_dict["Usage"] = usage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.assistant_message import AssistantMessage
        from ..models.cost import Cost
        from ..models.document import Document
        from ..models.options import Options
        from ..models.system_message import SystemMessage
        from ..models.tool_message import ToolMessage
        from ..models.usage import Usage
        from ..models.user_message import UserMessage

        d = src_dict.copy()
        _cost = d.pop("Cost", UNSET)
        cost: Union[Unset, Cost]
        if isinstance(_cost, Unset):
            cost = UNSET
        else:
            cost = Cost.from_dict(_cost)

        documents = []
        _documents = d.pop("Documents", UNSET)
        for documents_item_data in _documents or []:
            documents_item = Document.from_dict(documents_item_data)

            documents.append(documents_item)

        messages = []
        _messages = d.pop("Messages", UNSET)
        for messages_item_data in _messages or []:

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
        options: Union[Unset, Options]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = Options.from_dict(_options)

        _usage = d.pop("Usage", UNSET)
        usage: Union[Unset, Usage]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = Usage.from_dict(_usage)

        completion_family_data = cls(
            cost=cost,
            documents=documents,
            messages=messages,
            options=options,
            usage=usage,
        )

        return completion_family_data
