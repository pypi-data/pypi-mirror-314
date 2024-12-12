from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UsageValue")


@_attrs_define
class UsageValue:
    """
    Attributes:
        amount (float):
        unit (str):  Default: 'tokens'.
    """

    amount: float
    unit: str = "tokens"

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Amount": amount,
                "Unit": unit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        amount = d.pop("Amount")

        unit = d.pop("Unit")

        usage_value = cls(
            amount=amount,
            unit=unit,
        )

        return usage_value
