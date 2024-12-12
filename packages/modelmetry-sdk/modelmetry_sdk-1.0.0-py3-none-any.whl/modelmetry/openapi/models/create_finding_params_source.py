from typing import Literal, cast

CreateFindingParamsSource = Literal["annotation", "evaluator", "sdk"]

CREATE_FINDING_PARAMS_SOURCE_VALUES: set[CreateFindingParamsSource] = {
    "annotation",
    "evaluator",
    "sdk",
}


def check_create_finding_params_source(value: str) -> CreateFindingParamsSource:
    if value in CREATE_FINDING_PARAMS_SOURCE_VALUES:
        return cast(CreateFindingParamsSource, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_FINDING_PARAMS_SOURCE_VALUES!r}")
