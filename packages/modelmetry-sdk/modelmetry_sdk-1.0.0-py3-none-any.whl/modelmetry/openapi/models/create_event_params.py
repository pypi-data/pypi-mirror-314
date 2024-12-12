import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_event_params_metadata import CreateEventParamsMetadata


T = TypeVar("T", bound="CreateEventParams")


@_attrs_define
class CreateEventParams:
    """
    Attributes:
        name (str):
        xid (str):
        at (Union[None, Unset, datetime.datetime]):
        entry_id (Union[None, Unset, str]):
        metadata (Union[Unset, CreateEventParamsMetadata]):
        span_id (Union[None, Unset, str]):
        trace_id (Union[None, Unset, str]):
    """

    name: str
    xid: str
    at: Union[None, Unset, datetime.datetime] = UNSET
    entry_id: Union[None, Unset, str] = UNSET
    metadata: Union[Unset, "CreateEventParamsMetadata"] = UNSET
    span_id: Union[None, Unset, str] = UNSET
    trace_id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        xid = self.xid

        at: Union[None, Unset, str]
        if isinstance(self.at, Unset):
            at = UNSET
        elif isinstance(self.at, datetime.datetime):
            at = self.at.isoformat()
        else:
            at = self.at

        entry_id: Union[None, Unset, str]
        if isinstance(self.entry_id, Unset):
            entry_id = UNSET
        else:
            entry_id = self.entry_id

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        span_id: Union[None, Unset, str]
        if isinstance(self.span_id, Unset):
            span_id = UNSET
        else:
            span_id = self.span_id

        trace_id: Union[None, Unset, str]
        if isinstance(self.trace_id, Unset):
            trace_id = UNSET
        else:
            trace_id = self.trace_id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Name": name,
                "XID": xid,
            }
        )
        if at is not UNSET:
            field_dict["At"] = at
        if entry_id is not UNSET:
            field_dict["EntryID"] = entry_id
        if metadata is not UNSET:
            field_dict["Metadata"] = metadata
        if span_id is not UNSET:
            field_dict["SpanID"] = span_id
        if trace_id is not UNSET:
            field_dict["TraceID"] = trace_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_event_params_metadata import CreateEventParamsMetadata

        d = src_dict.copy()
        name = d.pop("Name")

        xid = d.pop("XID")

        def _parse_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                at_type_0 = isoparse(data)

                return at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        at = _parse_at(d.pop("At", UNSET))

        def _parse_entry_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        entry_id = _parse_entry_id(d.pop("EntryID", UNSET))

        _metadata = d.pop("Metadata", UNSET)
        metadata: Union[Unset, CreateEventParamsMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreateEventParamsMetadata.from_dict(_metadata)

        def _parse_span_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        span_id = _parse_span_id(d.pop("SpanID", UNSET))

        def _parse_trace_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        trace_id = _parse_trace_id(d.pop("TraceID", UNSET))

        create_event_params = cls(
            name=name,
            xid=xid,
            at=at,
            entry_id=entry_id,
            metadata=metadata,
            span_id=span_id,
            trace_id=trace_id,
        )

        return create_event_params
