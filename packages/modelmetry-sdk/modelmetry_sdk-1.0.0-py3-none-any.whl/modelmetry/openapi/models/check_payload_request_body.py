from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payload import Payload


T = TypeVar("T", bound="CheckPayloadRequestBody")


@_attrs_define
class CheckPayloadRequestBody:
    """
    Attributes:
        guardrail_id (str):
        payload (Payload):
        schema (Union[Unset, str]): A URL to the JSON Schema for this object.
        tenant_id (Union[Unset, str]):
    """

    guardrail_id: str
    payload: "Payload"
    schema: Union[Unset, str] = UNSET
    tenant_id: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        guardrail_id = self.guardrail_id

        payload = self.payload.to_dict()

        schema = self.schema

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "GuardrailID": guardrail_id,
                "Payload": payload,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if tenant_id is not UNSET:
            field_dict["TenantID"] = tenant_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.payload import Payload

        d = src_dict.copy()
        guardrail_id = d.pop("GuardrailID")

        payload = Payload.from_dict(d.pop("Payload"))

        schema = d.pop("$schema", UNSET)

        tenant_id = d.pop("TenantID", UNSET)

        check_payload_request_body = cls(
            guardrail_id=guardrail_id,
            payload=payload,
            schema=schema,
            tenant_id=tenant_id,
        )

        return check_payload_request_body
