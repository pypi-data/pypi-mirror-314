from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.payload import Payload


T = TypeVar("T", bound="EvaluateRequestByInstance")


@_attrs_define
class EvaluateRequestByInstance:
    """
    Attributes:
        instance_id (str):
        payload (Payload):
    """

    instance_id: str
    payload: "Payload"

    def to_dict(self) -> dict[str, Any]:
        instance_id = self.instance_id

        payload = self.payload.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "InstanceID": instance_id,
                "Payload": payload,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.payload import Payload

        d = src_dict.copy()
        instance_id = d.pop("InstanceID")

        payload = Payload.from_dict(d.pop("Payload"))

        evaluate_request_by_instance = cls(
            instance_id=instance_id,
            payload=payload,
        )

        return evaluate_request_by_instance
