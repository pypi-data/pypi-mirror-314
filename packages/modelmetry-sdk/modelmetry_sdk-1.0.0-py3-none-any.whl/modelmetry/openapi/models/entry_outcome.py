from typing import Literal, cast

EntryOutcome = Literal["error", "fail", "na", "pass", "pending", "skip"]

ENTRY_OUTCOME_VALUES: set[EntryOutcome] = {
    "error",
    "fail",
    "na",
    "pass",
    "pending",
    "skip",
}


def check_entry_outcome(value: str) -> EntryOutcome:
    if value in ENTRY_OUTCOME_VALUES:
        return cast(EntryOutcome, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ENTRY_OUTCOME_VALUES!r}")
