from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.assistant_message_role import AssistantMessageRole, check_assistant_message_role
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_part import DataPart
    from ..models.text_part import TextPart
    from ..models.tool_call import ToolCall


T = TypeVar("T", bound="AssistantMessage")


@_attrs_define
class AssistantMessage:
    """
    Attributes:
        contents (list[Union['DataPart', 'TextPart']]):
        role (AssistantMessageRole):
        name (Union[Unset, str]):
        tool_calls (Union[None, Unset, list['ToolCall']]):
    """

    contents: list[Union["DataPart", "TextPart"]]
    role: AssistantMessageRole
    name: Union[Unset, str] = UNSET
    tool_calls: Union[None, Unset, list["ToolCall"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.text_part import TextPart

        contents = []
        for contents_item_data in self.contents:
            contents_item: dict[str, Any]
            if isinstance(contents_item_data, TextPart):
                contents_item = contents_item_data.to_dict()
            else:
                contents_item = contents_item_data.to_dict()

            contents.append(contents_item)

        role: str = self.role

        name = self.name

        tool_calls: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.tool_calls, Unset):
            tool_calls = UNSET
        elif isinstance(self.tool_calls, list):
            tool_calls = []
            for tool_calls_type_0_item_data in self.tool_calls:
                tool_calls_type_0_item = tool_calls_type_0_item_data.to_dict()
                tool_calls.append(tool_calls_type_0_item)

        else:
            tool_calls = self.tool_calls

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Contents": contents,
                "Role": role,
            }
        )
        if name is not UNSET:
            field_dict["Name"] = name
        if tool_calls is not UNSET:
            field_dict["ToolCalls"] = tool_calls

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.data_part import DataPart
        from ..models.text_part import TextPart
        from ..models.tool_call import ToolCall

        d = src_dict.copy()
        contents = []
        _contents = d.pop("Contents")
        for contents_item_data in _contents:

            def _parse_contents_item(data: object) -> Union["DataPart", "TextPart"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    contents_item_type_0 = TextPart.from_dict(data)

                    return contents_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                contents_item_type_1 = DataPart.from_dict(data)

                return contents_item_type_1

            contents_item = _parse_contents_item(contents_item_data)

            contents.append(contents_item)

        role = check_assistant_message_role(d.pop("Role"))

        name = d.pop("Name", UNSET)

        def _parse_tool_calls(data: object) -> Union[None, Unset, list["ToolCall"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tool_calls_type_0 = []
                _tool_calls_type_0 = data
                for tool_calls_type_0_item_data in _tool_calls_type_0:
                    tool_calls_type_0_item = ToolCall.from_dict(tool_calls_type_0_item_data)

                    tool_calls_type_0.append(tool_calls_type_0_item)

                return tool_calls_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["ToolCall"]], data)

        tool_calls = _parse_tool_calls(d.pop("ToolCalls", UNSET))

        assistant_message = cls(
            contents=contents,
            role=role,
            name=name,
            tool_calls=tool_calls,
        )

        return assistant_message
