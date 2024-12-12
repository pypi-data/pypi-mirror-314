import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.event import Event
    from ..models.finding import Finding
    from ..models.full_trace_metadata import FullTraceMetadata
    from ..models.span import Span


T = TypeVar("T", bound="FullTrace")


@_attrs_define
class FullTrace:
    """
    Attributes:
        created_at (datetime.datetime):
        end (datetime.datetime):
        events (Union[None, list['Event']]):
        findings (Union[None, list['Finding']]):
        id (str):
        metadata (FullTraceMetadata):
        name (str):
        spans (Union[None, list['Span']]):
        start (datetime.datetime):
        tenant_id (str):
        updated_at (datetime.datetime):
        xid (str):
        session_id (Union[None, Unset, str]):
    """

    created_at: datetime.datetime
    end: datetime.datetime
    events: Union[None, list["Event"]]
    findings: Union[None, list["Finding"]]
    id: str
    metadata: "FullTraceMetadata"
    name: str
    spans: Union[None, list["Span"]]
    start: datetime.datetime
    tenant_id: str
    updated_at: datetime.datetime
    xid: str
    session_id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        end = self.end.isoformat()

        events: Union[None, list[dict[str, Any]]]
        if isinstance(self.events, list):
            events = []
            for events_type_0_item_data in self.events:
                events_type_0_item = events_type_0_item_data.to_dict()
                events.append(events_type_0_item)

        else:
            events = self.events

        findings: Union[None, list[dict[str, Any]]]
        if isinstance(self.findings, list):
            findings = []
            for findings_type_0_item_data in self.findings:
                findings_type_0_item = findings_type_0_item_data.to_dict()
                findings.append(findings_type_0_item)

        else:
            findings = self.findings

        id = self.id

        metadata = self.metadata.to_dict()

        name = self.name

        spans: Union[None, list[dict[str, Any]]]
        if isinstance(self.spans, list):
            spans = []
            for spans_type_0_item_data in self.spans:
                spans_type_0_item = spans_type_0_item_data.to_dict()
                spans.append(spans_type_0_item)

        else:
            spans = self.spans

        start = self.start.isoformat()

        tenant_id = self.tenant_id

        updated_at = self.updated_at.isoformat()

        xid = self.xid

        session_id: Union[None, Unset, str]
        if isinstance(self.session_id, Unset):
            session_id = UNSET
        else:
            session_id = self.session_id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "CreatedAt": created_at,
                "End": end,
                "Events": events,
                "Findings": findings,
                "ID": id,
                "Metadata": metadata,
                "Name": name,
                "Spans": spans,
                "Start": start,
                "TenantID": tenant_id,
                "UpdatedAt": updated_at,
                "XID": xid,
            }
        )
        if session_id is not UNSET:
            field_dict["SessionID"] = session_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.event import Event
        from ..models.finding import Finding
        from ..models.full_trace_metadata import FullTraceMetadata
        from ..models.span import Span

        d = src_dict.copy()
        created_at = isoparse(d.pop("CreatedAt"))

        end = isoparse(d.pop("End"))

        def _parse_events(data: object) -> Union[None, list["Event"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                events_type_0 = []
                _events_type_0 = data
                for events_type_0_item_data in _events_type_0:
                    events_type_0_item = Event.from_dict(events_type_0_item_data)

                    events_type_0.append(events_type_0_item)

                return events_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["Event"]], data)

        events = _parse_events(d.pop("Events"))

        def _parse_findings(data: object) -> Union[None, list["Finding"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                findings_type_0 = []
                _findings_type_0 = data
                for findings_type_0_item_data in _findings_type_0:
                    findings_type_0_item = Finding.from_dict(findings_type_0_item_data)

                    findings_type_0.append(findings_type_0_item)

                return findings_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["Finding"]], data)

        findings = _parse_findings(d.pop("Findings"))

        id = d.pop("ID")

        metadata = FullTraceMetadata.from_dict(d.pop("Metadata"))

        name = d.pop("Name")

        def _parse_spans(data: object) -> Union[None, list["Span"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                spans_type_0 = []
                _spans_type_0 = data
                for spans_type_0_item_data in _spans_type_0:
                    spans_type_0_item = Span.from_dict(spans_type_0_item_data)

                    spans_type_0.append(spans_type_0_item)

                return spans_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["Span"]], data)

        spans = _parse_spans(d.pop("Spans"))

        start = isoparse(d.pop("Start"))

        tenant_id = d.pop("TenantID")

        updated_at = isoparse(d.pop("UpdatedAt"))

        xid = d.pop("XID")

        def _parse_session_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        session_id = _parse_session_id(d.pop("SessionID", UNSET))

        full_trace = cls(
            created_at=created_at,
            end=end,
            events=events,
            findings=findings,
            id=id,
            metadata=metadata,
            name=name,
            spans=spans,
            start=start,
            tenant_id=tenant_id,
            updated_at=updated_at,
            xid=xid,
            session_id=session_id,
        )

        return full_trace
