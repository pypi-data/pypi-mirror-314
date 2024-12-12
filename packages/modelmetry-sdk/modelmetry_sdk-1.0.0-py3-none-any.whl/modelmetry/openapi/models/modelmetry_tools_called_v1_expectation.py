from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ModelmetryToolsCalledV1Expectation")


@_attrs_define
class ModelmetryToolsCalledV1Expectation:
    """
    Attributes:
        expression (str): The expression to check the tool call's arguements against
        name (str): The name of the tool call
    """

    expression: str
    name: str

    def to_dict(self) -> dict[str, Any]:
        expression = self.expression

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Expression": expression,
                "Name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        expression = d.pop("Expression")

        name = d.pop("Name")

        modelmetry_tools_called_v1_expectation = cls(
            expression=expression,
            name=name,
        )

        return modelmetry_tools_called_v1_expectation
