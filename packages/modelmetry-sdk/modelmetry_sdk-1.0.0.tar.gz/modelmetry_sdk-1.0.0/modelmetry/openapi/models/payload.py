from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.completion_payload import CompletionPayload


T = TypeVar("T", bound="Payload")


@_attrs_define
class Payload:
    """
    Attributes:
        completion (Union[Unset, CompletionPayload]):
    """

    completion: Union[Unset, "CompletionPayload"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        completion: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.completion, Unset):
            completion = self.completion.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if completion is not UNSET:
            field_dict["Completion"] = completion

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.completion_payload import CompletionPayload

        d = src_dict.copy()
        _completion = d.pop("Completion", UNSET)
        completion: Union[Unset, CompletionPayload]
        if isinstance(_completion, Unset):
            completion = UNSET
        else:
            completion = CompletionPayload.from_dict(_completion)

        payload = cls(
            completion=completion,
        )

        return payload
