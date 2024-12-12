from typing import Literal, cast

DataPartDetail = Literal["auto", "high", "low"]

DATA_PART_DETAIL_VALUES: set[DataPartDetail] = {
    "auto",
    "high",
    "low",
}


def check_data_part_detail(value: str) -> DataPartDetail:
    if value in DATA_PART_DETAIL_VALUES:
        return cast(DataPartDetail, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATA_PART_DETAIL_VALUES!r}")
