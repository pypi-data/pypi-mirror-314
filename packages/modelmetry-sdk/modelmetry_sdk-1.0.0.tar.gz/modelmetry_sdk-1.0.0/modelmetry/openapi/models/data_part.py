from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..models.data_part_detail import DataPartDetail, check_data_part_detail
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataPart")


@_attrs_define
class DataPart:
    """
    Attributes:
        data (str):
        mime_type (str):
        detail (Union[Unset, DataPartDetail]):
    """

    data: str
    mime_type: str
    detail: Union[Unset, DataPartDetail] = UNSET

    def to_dict(self) -> dict[str, Any]:
        data = self.data

        mime_type = self.mime_type

        detail: Union[Unset, str] = UNSET
        if not isinstance(self.detail, Unset):
            detail = self.detail

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Data": data,
                "MimeType": mime_type,
            }
        )
        if detail is not UNSET:
            field_dict["Detail"] = detail

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        data = d.pop("Data")

        mime_type = d.pop("MimeType")

        _detail = d.pop("Detail", UNSET)
        detail: Union[Unset, DataPartDetail]
        if isinstance(_detail, Unset):
            detail = UNSET
        else:
            detail = check_data_part_detail(_detail)

        data_part = cls(
            data=data,
            mime_type=mime_type,
            detail=detail,
        )

        return data_part
