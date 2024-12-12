from typing import Literal, cast

SimplifiedFindingSource = Literal["annotation", "evaluator", "sdk"]

SIMPLIFIED_FINDING_SOURCE_VALUES: set[SimplifiedFindingSource] = {
    "annotation",
    "evaluator",
    "sdk",
}


def check_simplified_finding_source(value: str) -> SimplifiedFindingSource:
    if value in SIMPLIFIED_FINDING_SOURCE_VALUES:
        return cast(SimplifiedFindingSource, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SIMPLIFIED_FINDING_SOURCE_VALUES!r}")
