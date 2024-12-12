from typing import Literal, cast

AssessmentAction = Literal["fail", "pass", "skip"]

ASSESSMENT_ACTION_VALUES: set[AssessmentAction] = {
    "fail",
    "pass",
    "skip",
}


def check_assessment_action(value: str) -> AssessmentAction:
    if value in ASSESSMENT_ACTION_VALUES:
        return cast(AssessmentAction, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ASSESSMENT_ACTION_VALUES!r}")
