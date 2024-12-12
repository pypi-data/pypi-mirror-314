from typing import Literal, cast

FindingSource = Literal["annotation", "evaluator", "sdk"]

FINDING_SOURCE_VALUES: set[FindingSource] = {
    "annotation",
    "evaluator",
    "sdk",
}


def check_finding_source(value: str) -> FindingSource:
    if value in FINDING_SOURCE_VALUES:
        return cast(FindingSource, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FINDING_SOURCE_VALUES!r}")
