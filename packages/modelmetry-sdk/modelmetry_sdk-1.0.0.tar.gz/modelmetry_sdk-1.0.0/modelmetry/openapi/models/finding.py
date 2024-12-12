import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.finding_source import FindingSource, check_finding_source
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.finding_metadata import FindingMetadata


T = TypeVar("T", bound="Finding")


@_attrs_define
class Finding:
    """
    Attributes:
        comment (str):
        created_at (datetime.datetime):
        evaluator_id (Union[None, str]):
        id (str):
        metadata (FindingMetadata):
        name (str):
        source (FindingSource):  Default: 'annotation'.
        tenant_id (str):
        unit (str):
        updated_at (datetime.datetime):
        value (Union[bool, float, str]):
        xid (str):
        check_id (Union[Unset, str]):
        entry_id (Union[Unset, str]):
        span_id (Union[Unset, str]):
        trace_id (Union[Unset, str]):
    """

    comment: str
    created_at: datetime.datetime
    evaluator_id: Union[None, str]
    id: str
    metadata: "FindingMetadata"
    name: str
    tenant_id: str
    unit: str
    updated_at: datetime.datetime
    value: Union[bool, float, str]
    xid: str
    source: FindingSource = "annotation"
    check_id: Union[Unset, str] = UNSET
    entry_id: Union[Unset, str] = UNSET
    span_id: Union[Unset, str] = UNSET
    trace_id: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        comment = self.comment

        created_at = self.created_at.isoformat()

        evaluator_id: Union[None, str]
        evaluator_id = self.evaluator_id

        id = self.id

        metadata = self.metadata.to_dict()

        name = self.name

        source: str = self.source

        tenant_id = self.tenant_id

        unit = self.unit

        updated_at = self.updated_at.isoformat()

        value: Union[bool, float, str]
        value = self.value

        xid = self.xid

        check_id = self.check_id

        entry_id = self.entry_id

        span_id = self.span_id

        trace_id = self.trace_id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Comment": comment,
                "CreatedAt": created_at,
                "EvaluatorID": evaluator_id,
                "ID": id,
                "Metadata": metadata,
                "Name": name,
                "Source": source,
                "TenantID": tenant_id,
                "Unit": unit,
                "UpdatedAt": updated_at,
                "Value": value,
                "XID": xid,
            }
        )
        if check_id is not UNSET:
            field_dict["CheckID"] = check_id
        if entry_id is not UNSET:
            field_dict["EntryID"] = entry_id
        if span_id is not UNSET:
            field_dict["SpanID"] = span_id
        if trace_id is not UNSET:
            field_dict["TraceID"] = trace_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.finding_metadata import FindingMetadata

        d = src_dict.copy()
        comment = d.pop("Comment")

        created_at = isoparse(d.pop("CreatedAt"))

        def _parse_evaluator_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        evaluator_id = _parse_evaluator_id(d.pop("EvaluatorID"))

        id = d.pop("ID")

        metadata = FindingMetadata.from_dict(d.pop("Metadata"))

        name = d.pop("Name")

        source = check_finding_source(d.pop("Source"))

        tenant_id = d.pop("TenantID")

        unit = d.pop("Unit")

        updated_at = isoparse(d.pop("UpdatedAt"))

        def _parse_value(data: object) -> Union[bool, float, str]:
            return cast(Union[bool, float, str], data)

        value = _parse_value(d.pop("Value"))

        xid = d.pop("XID")

        check_id = d.pop("CheckID", UNSET)

        entry_id = d.pop("EntryID", UNSET)

        span_id = d.pop("SpanID", UNSET)

        trace_id = d.pop("TraceID", UNSET)

        finding = cls(
            comment=comment,
            created_at=created_at,
            evaluator_id=evaluator_id,
            id=id,
            metadata=metadata,
            name=name,
            source=source,
            tenant_id=tenant_id,
            unit=unit,
            updated_at=updated_at,
            value=value,
            xid=xid,
            check_id=check_id,
            entry_id=entry_id,
            span_id=span_id,
            trace_id=trace_id,
        )

        return finding
