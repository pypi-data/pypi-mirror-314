from typing import Literal, cast

SummarisedEntryOutcome = Literal["error", "fail", "na", "pass", "pending", "skip"]

SUMMARISED_ENTRY_OUTCOME_VALUES: set[SummarisedEntryOutcome] = {
    "error",
    "fail",
    "na",
    "pass",
    "pending",
    "skip",
}


def check_summarised_entry_outcome(value: str) -> SummarisedEntryOutcome:
    if value in SUMMARISED_ENTRY_OUTCOME_VALUES:
        return cast(SummarisedEntryOutcome, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SUMMARISED_ENTRY_OUTCOME_VALUES!r}")
