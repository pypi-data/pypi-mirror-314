from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.assessment import Assessment


T = TypeVar("T", bound="GradingConfiguration")


@_attrs_define
class GradingConfiguration:
    """
    Attributes:
        assessments (list['Assessment']):
    """

    assessments: list["Assessment"]

    def to_dict(self) -> dict[str, Any]:
        assessments = []
        for assessments_item_data in self.assessments:
            assessments_item = assessments_item_data.to_dict()
            assessments.append(assessments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Assessments": assessments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.assessment import Assessment

        d = src_dict.copy()
        assessments = []
        _assessments = d.pop("Assessments")
        for assessments_item_data in _assessments:
            assessments_item = Assessment.from_dict(assessments_item_data)

            assessments.append(assessments_item)

        grading_configuration = cls(
            assessments=assessments,
        )

        return grading_configuration
