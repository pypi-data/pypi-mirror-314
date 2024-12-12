from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="Money")


@_attrs_define
class Money:
    """
    Attributes:
        amount (float):
        currency (str):
    """

    amount: float
    currency: str

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        currency = self.currency

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Amount": amount,
                "Currency": currency,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        amount = d.pop("Amount")

        currency = d.pop("Currency")

        money = cls(
            amount=amount,
            currency=currency,
        )

        return money
