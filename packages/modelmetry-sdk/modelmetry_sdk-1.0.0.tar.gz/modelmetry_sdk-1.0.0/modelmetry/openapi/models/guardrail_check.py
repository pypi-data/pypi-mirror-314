import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.guardrail_check_outcome import GuardrailCheckOutcome, check_guardrail_check_outcome
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.guardrail_check_metadata import GuardrailCheckMetadata
    from ..models.payload import Payload
    from ..models.summarised_entry import SummarisedEntry


T = TypeVar("T", bound="GuardrailCheck")


@_attrs_define
class GuardrailCheck:
    """
    Attributes:
        created_at (datetime.datetime):
        created_by (str):
        duration_ms (int):
        guardrail_id (str):
        id (str):
        metadata (GuardrailCheckMetadata):
        outcome (GuardrailCheckOutcome): The status of the entry. Default: 'na'.
        payload (Payload):
        summarised_entries (Union[None, list['SummarisedEntry']]):
        tenant_id (str):
        updated_at (datetime.datetime):
        updated_by (str):
        schema (Union[Unset, str]): A URL to the JSON Schema for this object.
    """

    created_at: datetime.datetime
    created_by: str
    duration_ms: int
    guardrail_id: str
    id: str
    metadata: "GuardrailCheckMetadata"
    payload: "Payload"
    summarised_entries: Union[None, list["SummarisedEntry"]]
    tenant_id: str
    updated_at: datetime.datetime
    updated_by: str
    outcome: GuardrailCheckOutcome = "na"
    schema: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by = self.created_by

        duration_ms = self.duration_ms

        guardrail_id = self.guardrail_id

        id = self.id

        metadata = self.metadata.to_dict()

        outcome: str = self.outcome

        payload = self.payload.to_dict()

        summarised_entries: Union[None, list[dict[str, Any]]]
        if isinstance(self.summarised_entries, list):
            summarised_entries = []
            for summarised_entries_type_0_item_data in self.summarised_entries:
                summarised_entries_type_0_item = summarised_entries_type_0_item_data.to_dict()
                summarised_entries.append(summarised_entries_type_0_item)

        else:
            summarised_entries = self.summarised_entries

        tenant_id = self.tenant_id

        updated_at = self.updated_at.isoformat()

        updated_by = self.updated_by

        schema = self.schema

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "CreatedAt": created_at,
                "CreatedBy": created_by,
                "DurationMs": duration_ms,
                "GuardrailID": guardrail_id,
                "ID": id,
                "Metadata": metadata,
                "Outcome": outcome,
                "Payload": payload,
                "SummarisedEntries": summarised_entries,
                "TenantID": tenant_id,
                "UpdatedAt": updated_at,
                "UpdatedBy": updated_by,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.guardrail_check_metadata import GuardrailCheckMetadata
        from ..models.payload import Payload
        from ..models.summarised_entry import SummarisedEntry

        d = src_dict.copy()
        created_at = isoparse(d.pop("CreatedAt"))

        created_by = d.pop("CreatedBy")

        duration_ms = d.pop("DurationMs")

        guardrail_id = d.pop("GuardrailID")

        id = d.pop("ID")

        metadata = GuardrailCheckMetadata.from_dict(d.pop("Metadata"))

        outcome = check_guardrail_check_outcome(d.pop("Outcome"))

        payload = Payload.from_dict(d.pop("Payload"))

        def _parse_summarised_entries(data: object) -> Union[None, list["SummarisedEntry"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                summarised_entries_type_0 = []
                _summarised_entries_type_0 = data
                for summarised_entries_type_0_item_data in _summarised_entries_type_0:
                    summarised_entries_type_0_item = SummarisedEntry.from_dict(summarised_entries_type_0_item_data)

                    summarised_entries_type_0.append(summarised_entries_type_0_item)

                return summarised_entries_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["SummarisedEntry"]], data)

        summarised_entries = _parse_summarised_entries(d.pop("SummarisedEntries"))

        tenant_id = d.pop("TenantID")

        updated_at = isoparse(d.pop("UpdatedAt"))

        updated_by = d.pop("UpdatedBy")

        schema = d.pop("$schema", UNSET)

        guardrail_check = cls(
            created_at=created_at,
            created_by=created_by,
            duration_ms=duration_ms,
            guardrail_id=guardrail_id,
            id=id,
            metadata=metadata,
            outcome=outcome,
            payload=payload,
            summarised_entries=summarised_entries,
            tenant_id=tenant_id,
            updated_at=updated_at,
            updated_by=updated_by,
            schema=schema,
        )

        return guardrail_check
