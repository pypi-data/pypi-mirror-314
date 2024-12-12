from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..models.system_message_role import SystemMessageRole, check_system_message_role
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_part import DataPart
    from ..models.text_part import TextPart


T = TypeVar("T", bound="SystemMessage")


@_attrs_define
class SystemMessage:
    """
    Attributes:
        contents (list[Union['DataPart', 'TextPart']]):
        role (SystemMessageRole):
        name (Union[Unset, str]):
    """

    contents: list[Union["DataPart", "TextPart"]]
    role: SystemMessageRole
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

        role = check_system_message_role(d.pop("Role"))

        name = d.pop("Name", UNSET)

        system_message = cls(
            contents=contents,
            role=role,
            name=name,
        )

        return system_message
