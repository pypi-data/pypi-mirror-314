from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.assessment_action import AssessmentAction, check_assessment_action

T = TypeVar("T", bound="Assessment")


@_attrs_define
class Assessment:
    """
    Attributes:
        action (AssessmentAction):  Default: 'pass'.
        expression (str):
        id (str):
        message (str):
    """

    expression: str
    id: str
    message: str
    action: AssessmentAction = "pass"

    def to_dict(self) -> dict[str, Any]:
        action: str = self.action

        expression = self.expression

        id = self.id

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Action": action,
                "Expression": expression,
                "ID": id,
                "Message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        action = check_assessment_action(d.pop("Action"))

        expression = d.pop("Expression")

        id = d.pop("ID")

        message = d.pop("Message")

        assessment = cls(
            action=action,
            expression=expression,
            id=id,
            message=message,
        )

        return assessment
