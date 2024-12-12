from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.modelmetry_tools_called_v1_expectation import ModelmetryToolsCalledV1Expectation


T = TypeVar("T", bound="ModelmetryToolsCalledV1Config")


@_attrs_define
class ModelmetryToolsCalledV1Config:
    """
    Attributes:
        expections (list['ModelmetryToolsCalledV1Expectation']): The expected JSON schema to validate against
        expectations (Union[Unset, Any]):
    """

    expections: list["ModelmetryToolsCalledV1Expectation"]
    expectations: Union[Unset, Any] = UNSET

    def to_dict(self) -> dict[str, Any]:
        expections = []
        for expections_item_data in self.expections:
            expections_item = expections_item_data.to_dict()
            expections.append(expections_item)

        expectations = self.expectations

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Expections": expections,
            }
        )
        if expectations is not UNSET:
            field_dict["Expectations"] = expectations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.modelmetry_tools_called_v1_expectation import ModelmetryToolsCalledV1Expectation

        d = src_dict.copy()
        expections = []
        _expections = d.pop("Expections")
        for expections_item_data in _expections:
            expections_item = ModelmetryToolsCalledV1Expectation.from_dict(expections_item_data)

            expections.append(expections_item)

        expectations = d.pop("Expectations", UNSET)

        modelmetry_tools_called_v1_config = cls(
            expections=expections,
            expectations=expectations,
        )

        return modelmetry_tools_called_v1_config
