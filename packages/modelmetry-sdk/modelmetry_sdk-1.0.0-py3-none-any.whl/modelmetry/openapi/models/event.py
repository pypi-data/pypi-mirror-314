import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.event_metadata import EventMetadata


T = TypeVar("T", bound="Event")


@_attrs_define
class Event:
    """
    Attributes:
        created_at (datetime.datetime):
        entry_id (Union[None, str]):
        id (str):
        metadata (EventMetadata):
        name (str):
        span_id (Union[None, str]):
        tenant_id (str):
        trace_id (Union[None, str]):
        updated_at (datetime.datetime):
        xid (str):
    """

    created_at: datetime.datetime
    entry_id: Union[None, str]
    id: str
    metadata: "EventMetadata"
    name: str
    span_id: Union[None, str]
    tenant_id: str
    trace_id: Union[None, str]
    updated_at: datetime.datetime
    xid: str

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        entry_id: Union[None, str]
        entry_id = self.entry_id

        id = self.id

        metadata = self.metadata.to_dict()

        name = self.name

        span_id: Union[None, str]
        span_id = self.span_id

        tenant_id = self.tenant_id

        trace_id: Union[None, str]
        trace_id = self.trace_id

        updated_at = self.updated_at.isoformat()

        xid = self.xid

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "CreatedAt": created_at,
                "EntryID": entry_id,
                "ID": id,
                "Metadata": metadata,
                "Name": name,
                "SpanID": span_id,
                "TenantID": tenant_id,
                "TraceID": trace_id,
                "UpdatedAt": updated_at,
                "XID": xid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.event_metadata import EventMetadata

        d = src_dict.copy()
        created_at = isoparse(d.pop("CreatedAt"))

        def _parse_entry_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        entry_id = _parse_entry_id(d.pop("EntryID"))

        id = d.pop("ID")

        metadata = EventMetadata.from_dict(d.pop("Metadata"))

        name = d.pop("Name")

        def _parse_span_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        span_id = _parse_span_id(d.pop("SpanID"))

        tenant_id = d.pop("TenantID")

        def _parse_trace_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        trace_id = _parse_trace_id(d.pop("TraceID"))

        updated_at = isoparse(d.pop("UpdatedAt"))

        xid = d.pop("XID")

        event = cls(
            created_at=created_at,
            entry_id=entry_id,
            id=id,
            metadata=metadata,
            name=name,
            span_id=span_id,
            tenant_id=tenant_id,
            trace_id=trace_id,
            updated_at=updated_at,
            xid=xid,
        )

        return event
