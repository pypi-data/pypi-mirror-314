from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="Function")


@_attrs_define
class Function:
    """
    Attributes:
        arguments (Any):
        name (str):
    """

    arguments: Any
    name: str

    def to_dict(self) -> dict[str, Any]:
        arguments = self.arguments

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Arguments": arguments,
                "Name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        arguments = d.pop("Arguments")

        name = d.pop("Name")

        function = cls(
            arguments=arguments,
            name=name,
        )

        return function
