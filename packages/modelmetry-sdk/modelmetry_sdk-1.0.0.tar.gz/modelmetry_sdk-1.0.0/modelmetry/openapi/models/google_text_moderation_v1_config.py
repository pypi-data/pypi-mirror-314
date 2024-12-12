from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.google_text_moderation_v1_config_attributes_type_0_item import (
    GoogleTextModerationV1ConfigAttributesType0Item,
    check_google_text_moderation_v1_config_attributes_type_0_item,
)

T = TypeVar("T", bound="GoogleTextModerationV1Config")


@_attrs_define
class GoogleTextModerationV1Config:
    """
    Attributes:
        attributes (Union[None, list[GoogleTextModerationV1ConfigAttributesType0Item]]): The attributes to check for. An
            empty list will check for all attributes.
    """

    attributes: Union[None, list[GoogleTextModerationV1ConfigAttributesType0Item]]

    def to_dict(self) -> dict[str, Any]:
        attributes: Union[None, list[str]]
        if isinstance(self.attributes, list):
            attributes = []
            for attributes_type_0_item_data in self.attributes:
                attributes_type_0_item: str = attributes_type_0_item_data
                attributes.append(attributes_type_0_item)

        else:
            attributes = self.attributes

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_attributes(data: object) -> Union[None, list[GoogleTextModerationV1ConfigAttributesType0Item]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                attributes_type_0 = []
                _attributes_type_0 = data
                for attributes_type_0_item_data in _attributes_type_0:
                    attributes_type_0_item = check_google_text_moderation_v1_config_attributes_type_0_item(
                        attributes_type_0_item_data
                    )

                    attributes_type_0.append(attributes_type_0_item)

                return attributes_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[GoogleTextModerationV1ConfigAttributesType0Item]], data)

        attributes = _parse_attributes(d.pop("Attributes"))

        google_text_moderation_v1_config = cls(
            attributes=attributes,
        )

        return google_text_moderation_v1_config
