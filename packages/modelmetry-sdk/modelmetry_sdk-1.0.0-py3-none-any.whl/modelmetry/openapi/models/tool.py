from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="Tool")


@_attrs_define
class Tool:
    """
    Attributes:
        description (str):
        name (str):
        parameters (Any):
    """

    description: str
    name: str
    parameters: Any

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        name = self.name

        parameters = self.parameters

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Description": description,
                "Name": name,
                "Parameters": parameters,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("Description")

        name = d.pop("Name")

        parameters = d.pop("Parameters")

        tool = cls(
            description=description,
            name=name,
            parameters=parameters,
        )

        return tool
