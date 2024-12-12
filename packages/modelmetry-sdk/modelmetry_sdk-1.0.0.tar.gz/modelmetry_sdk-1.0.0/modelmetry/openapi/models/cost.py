from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.money import Money


T = TypeVar("T", bound="Cost")


@_attrs_define
class Cost:
    """
    Attributes:
        input_ (Union[Unset, Money]):
        output (Union[Unset, Money]):
        total (Union[Unset, Money]):
    """

    input_: Union[Unset, "Money"] = UNSET
    output: Union[Unset, "Money"] = UNSET
    total: Union[Unset, "Money"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        input_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.input_, Unset):
            input_ = self.input_.to_dict()

        output: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.output, Unset):
            output = self.output.to_dict()

        total: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.total, Unset):
            total = self.total.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if input_ is not UNSET:
            field_dict["Input"] = input_
        if output is not UNSET:
            field_dict["Output"] = output
        if total is not UNSET:
            field_dict["Total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.money import Money

        d = src_dict.copy()
        _input_ = d.pop("Input", UNSET)
        input_: Union[Unset, Money]
        if isinstance(_input_, Unset):
            input_ = UNSET
        else:
            input_ = Money.from_dict(_input_)

        _output = d.pop("Output", UNSET)
        output: Union[Unset, Money]
        if isinstance(_output, Unset):
            output = UNSET
        else:
            output = Money.from_dict(_output)

        _total = d.pop("Total", UNSET)
        total: Union[Unset, Money]
        if isinstance(_total, Unset):
            total = UNSET
        else:
            total = Money.from_dict(_total)

        cost = cls(
            input_=input_,
            output=output,
            total=total,
        )

        return cost
