from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..models.tool_message_role import ToolMessageRole, check_tool_message_role

if TYPE_CHECKING:
    from ..models.data_part import DataPart
    from ..models.text_part import TextPart


T = TypeVar("T", bound="ToolMessage")


@_attrs_define
class ToolMessage:
    """
    Attributes:
        contents (list[Union['DataPart', 'TextPart']]):
        role (ToolMessageRole):
        tool_call_id (str):
    """

    contents: list[Union["DataPart", "TextPart"]]
    role: ToolMessageRole
    tool_call_id: str

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

        tool_call_id = self.tool_call_id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Contents": contents,
                "Role": role,
                "ToolCallID": tool_call_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.data_part import DataPart
        from ..models.text_part import TextPart

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

        role = check_tool_message_role(d.pop("Role"))

        tool_call_id = d.pop("ToolCallID")

        tool_message = cls(
            contents=contents,
            role=role,
            tool_call_id=tool_call_id,
        )

        return tool_message
