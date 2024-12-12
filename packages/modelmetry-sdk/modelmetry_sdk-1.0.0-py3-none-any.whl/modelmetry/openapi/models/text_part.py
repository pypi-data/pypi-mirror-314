from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="TextPart")


@_attrs_define
class TextPart:
    """
    Attributes:
        text (str):
    """

    text: str

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        text = d.pop("Text")

        text_part = cls(
            text=text,
        )

        return text_part
