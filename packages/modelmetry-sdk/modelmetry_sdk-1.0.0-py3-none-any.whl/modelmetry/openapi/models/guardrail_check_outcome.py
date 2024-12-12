from typing import Literal, cast

GuardrailCheckOutcome = Literal["error", "fail", "na", "pass", "pending", "skip"]

GUARDRAIL_CHECK_OUTCOME_VALUES: set[GuardrailCheckOutcome] = {
    "error",
    "fail",
    "na",
    "pass",
    "pending",
    "skip",
}


def check_guardrail_check_outcome(value: str) -> GuardrailCheckOutcome:
    if value in GUARDRAIL_CHECK_OUTCOME_VALUES:
        return cast(GuardrailCheckOutcome, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GUARDRAIL_CHECK_OUTCOME_VALUES!r}")
