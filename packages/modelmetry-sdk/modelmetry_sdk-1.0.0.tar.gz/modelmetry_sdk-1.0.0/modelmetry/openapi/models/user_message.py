from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..models.user_message_role import UserMessageRole, check_user_message_role
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_part import DataPart
    from ..models.text_part import TextPart


T = TypeVar("T", bound="UserMessage")


@_attrs_define
class UserMessage:
    """
    Attributes:
        contents (list[Union['DataPart', 'TextPart']]):
        role (UserMessageRole):
        name (Union[Unset, str]):
    """

    contents: list[Union["DataPart", "TextPart"]]
    role: UserMessageRole
    name: Union[Unset, str] = UNSET

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

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Contents": contents,
                "Role": role,
            }
        )
        if name is not UNSET:
            field_dict["Name"] = name

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

        role = check_user_message_role(d.pop("Role"))

        name = d.pop("Name", UNSET)

        user_message = cls(
            contents=contents,
            role=role,
            name=name,
        )

        return user_message
