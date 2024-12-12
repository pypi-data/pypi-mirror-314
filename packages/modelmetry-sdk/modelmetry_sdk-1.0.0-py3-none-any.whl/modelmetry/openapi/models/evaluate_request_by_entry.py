from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="EvaluateRequestByEntry")


@_attrs_define
class EvaluateRequestByEntry:
    """
    Attributes:
        entry_id (str):
    """

    entry_id: str

    def to_dict(self) -> dict[str, Any]:
        entry_id = self.entry_id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "EntryID": entry_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        entry_id = d.pop("EntryID")

        evaluate_request_by_entry = cls(
            entry_id=entry_id,
        )

        return evaluate_request_by_entry
