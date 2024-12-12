import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.completion_family_data import CompletionFamilyData
    from ..models.embeddings_family_data import EmbeddingsFamilyData
    from ..models.event import Event
    from ..models.finding import Finding
    from ..models.other_family_data import OtherFamilyData
    from ..models.retrieval_family_data import RetrievalFamilyData
    from ..models.span_metadata import SpanMetadata


T = TypeVar("T", bound="Span")


@_attrs_define
class Span:
    """
    Attributes:
        created_at (datetime.datetime):
        end (datetime.datetime):
        events (Union[None, list['Event']]):
        family (str):
        findings (Union[None, list['Finding']]):
        id (str):
        message (str):
        metadata (SpanMetadata):
        name (str):
        parent_id (Union[None, str]):
        severity (str):
        start (datetime.datetime):
        tenant_id (str):
        trace_id (str):
        updated_at (datetime.datetime):
        xid (str):
        completion (Union[Unset, CompletionFamilyData]):
        embeddings (Union[Unset, EmbeddingsFamilyData]):
        other (Union[Unset, OtherFamilyData]):
        retrieval (Union[Unset, RetrievalFamilyData]):
    """

    created_at: datetime.datetime
    end: datetime.datetime
    events: Union[None, list["Event"]]
    family: str
    findings: Union[None, list["Finding"]]
    id: str
    message: str
    metadata: "SpanMetadata"
    name: str
    parent_id: Union[None, str]
    severity: str
    start: datetime.datetime
    tenant_id: str
    trace_id: str
    updated_at: datetime.datetime
    xid: str
    completion: Union[Unset, "CompletionFamilyData"] = UNSET
    embeddings: Union[Unset, "EmbeddingsFamilyData"] = UNSET
    other: Union[Unset, "OtherFamilyData"] = UNSET
    retrieval: Union[Unset, "RetrievalFamilyData"] = UNSET

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

        family = self.family

        findings: Union[None, list[dict[str, Any]]]
        if isinstance(self.findings, list):
            findings = []
            for findings_type_0_item_data in self.findings:
                findings_type_0_item = findings_type_0_item_data.to_dict()
                findings.append(findings_type_0_item)

        else:
            findings = self.findings

        id = self.id

        message = self.message

        metadata = self.metadata.to_dict()

        name = self.name

        parent_id: Union[None, str]
        parent_id = self.parent_id

        severity = self.severity

        start = self.start.isoformat()

        tenant_id = self.tenant_id

        trace_id = self.trace_id

        updated_at = self.updated_at.isoformat()

        xid = self.xid

        completion: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.completion, Unset):
            completion = self.completion.to_dict()

        embeddings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.embeddings, Unset):
            embeddings = self.embeddings.to_dict()

        other: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.other, Unset):
            other = self.other.to_dict()

        retrieval: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.retrieval, Unset):
            retrieval = self.retrieval.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "CreatedAt": created_at,
                "End": end,
                "Events": events,
                "Family": family,
                "Findings": findings,
                "ID": id,
                "Message": message,
                "Metadata": metadata,
                "Name": name,
                "ParentID": parent_id,
                "Severity": severity,
                "Start": start,
                "TenantID": tenant_id,
                "TraceID": trace_id,
                "UpdatedAt": updated_at,
                "XID": xid,
            }
        )
        if completion is not UNSET:
            field_dict["Completion"] = completion
        if embeddings is not UNSET:
            field_dict["Embeddings"] = embeddings
        if other is not UNSET:
            field_dict["Other"] = other
        if retrieval is not UNSET:
            field_dict["Retrieval"] = retrieval

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.completion_family_data import CompletionFamilyData
        from ..models.embeddings_family_data import EmbeddingsFamilyData
        from ..models.event import Event
        from ..models.finding import Finding
        from ..models.other_family_data import OtherFamilyData
        from ..models.retrieval_family_data import RetrievalFamilyData
        from ..models.span_metadata import SpanMetadata

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

        family = d.pop("Family")

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

        message = d.pop("Message")

        metadata = SpanMetadata.from_dict(d.pop("Metadata"))

        name = d.pop("Name")

        def _parse_parent_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        parent_id = _parse_parent_id(d.pop("ParentID"))

        severity = d.pop("Severity")

        start = isoparse(d.pop("Start"))

        tenant_id = d.pop("TenantID")

        trace_id = d.pop("TraceID")

        updated_at = isoparse(d.pop("UpdatedAt"))

        xid = d.pop("XID")

        _completion = d.pop("Completion", UNSET)
        completion: Union[Unset, CompletionFamilyData]
        if isinstance(_completion, Unset):
            completion = UNSET
        else:
            completion = CompletionFamilyData.from_dict(_completion)

        _embeddings = d.pop("Embeddings", UNSET)
        embeddings: Union[Unset, EmbeddingsFamilyData]
        if isinstance(_embeddings, Unset):
            embeddings = UNSET
        else:
            embeddings = EmbeddingsFamilyData.from_dict(_embeddings)

        _other = d.pop("Other", UNSET)
        other: Union[Unset, OtherFamilyData]
        if isinstance(_other, Unset):
            other = UNSET
        else:
            other = OtherFamilyData.from_dict(_other)

        _retrieval = d.pop("Retrieval", UNSET)
        retrieval: Union[Unset, RetrievalFamilyData]
        if isinstance(_retrieval, Unset):
            retrieval = UNSET
        else:
            retrieval = RetrievalFamilyData.from_dict(_retrieval)

        span = cls(
            created_at=created_at,
            end=end,
            events=events,
            family=family,
            findings=findings,
            id=id,
            message=message,
            metadata=metadata,
            name=name,
            parent_id=parent_id,
            severity=severity,
            start=start,
            tenant_id=tenant_id,
            trace_id=trace_id,
            updated_at=updated_at,
            xid=xid,
            completion=completion,
            embeddings=embeddings,
            other=other,
            retrieval=retrieval,
        )

        return span
