import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.entry_outcome import EntryOutcome, check_entry_outcome
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.entry_config import EntryConfig
    from ..models.entry_metadata import EntryMetadata
    from ..models.finding import Finding
    from ..models.grading_configuration import GradingConfiguration
    from ..models.payload import Payload


T = TypeVar("T", bound="Entry")


@_attrs_define
class Entry:
    """
    Attributes:
        check_id (Union[None, str]):
        config (EntryConfig):
        created_at (datetime.datetime):
        created_by (str):
        duration_ms (int):
        evaluator_id (str):
        findings (Union[None, list['Finding']]):
        finished_at (Union[None, datetime.datetime]):
        grading (GradingConfiguration):
        id (str):
        instance_id (Union[None, str]):
        message (str):
        metadata (EntryMetadata):
        outcome (EntryOutcome): The status of the entry. Default: 'na'.
        payload (Payload):
        skip (str):
        span_id (Union[None, str]):
        started_at (datetime.datetime):
        tenant_id (str):
        trace_id (Union[None, str]):
        updated_at (datetime.datetime):
        updated_by (str):
        schema (Union[Unset, str]): A URL to the JSON Schema for this object.
    """

    check_id: Union[None, str]
    config: "EntryConfig"
    created_at: datetime.datetime
    created_by: str
    duration_ms: int
    evaluator_id: str
    findings: Union[None, list["Finding"]]
    finished_at: Union[None, datetime.datetime]
    grading: "GradingConfiguration"
    id: str
    instance_id: Union[None, str]
    message: str
    metadata: "EntryMetadata"
    payload: "Payload"
    skip: str
    span_id: Union[None, str]
    started_at: datetime.datetime
    tenant_id: str
    trace_id: Union[None, str]
    updated_at: datetime.datetime
    updated_by: str
    outcome: EntryOutcome = "na"
    schema: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        check_id: Union[None, str]
        check_id = self.check_id

        config = self.config.to_dict()

        created_at = self.created_at.isoformat()

        created_by = self.created_by

        duration_ms = self.duration_ms

        evaluator_id = self.evaluator_id

        findings: Union[None, list[dict[str, Any]]]
        if isinstance(self.findings, list):
            findings = []
            for findings_type_0_item_data in self.findings:
                findings_type_0_item = findings_type_0_item_data.to_dict()
                findings.append(findings_type_0_item)

        else:
            findings = self.findings

        finished_at: Union[None, str]
        if isinstance(self.finished_at, datetime.datetime):
            finished_at = self.finished_at.isoformat()
        else:
            finished_at = self.finished_at

        grading = self.grading.to_dict()

        id = self.id

        instance_id: Union[None, str]
        instance_id = self.instance_id

        message = self.message

        metadata = self.metadata.to_dict()

        outcome: str = self.outcome

        payload = self.payload.to_dict()

        skip = self.skip

        span_id: Union[None, str]
        span_id = self.span_id

        started_at = self.started_at.isoformat()

        tenant_id = self.tenant_id

        trace_id: Union[None, str]
        trace_id = self.trace_id

        updated_at = self.updated_at.isoformat()

        updated_by = self.updated_by

        schema = self.schema

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "CheckID": check_id,
                "Config": config,
                "CreatedAt": created_at,
                "CreatedBy": created_by,
                "DurationMs": duration_ms,
                "EvaluatorID": evaluator_id,
                "Findings": findings,
                "FinishedAt": finished_at,
                "Grading": grading,
                "ID": id,
                "InstanceID": instance_id,
                "Message": message,
                "Metadata": metadata,
                "Outcome": outcome,
                "Payload": payload,
                "Skip": skip,
                "SpanID": span_id,
                "StartedAt": started_at,
                "TenantID": tenant_id,
                "TraceID": trace_id,
                "UpdatedAt": updated_at,
                "UpdatedBy": updated_by,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.entry_config import EntryConfig
        from ..models.entry_metadata import EntryMetadata
        from ..models.finding import Finding
        from ..models.grading_configuration import GradingConfiguration
        from ..models.payload import Payload

        d = src_dict.copy()

        def _parse_check_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        check_id = _parse_check_id(d.pop("CheckID"))

        config = EntryConfig.from_dict(d.pop("Config"))

        created_at = isoparse(d.pop("CreatedAt"))

        created_by = d.pop("CreatedBy")

        duration_ms = d.pop("DurationMs")

        evaluator_id = d.pop("EvaluatorID")

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

        def _parse_finished_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finished_at_type_0 = isoparse(data)

                return finished_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        finished_at = _parse_finished_at(d.pop("FinishedAt"))

        grading = GradingConfiguration.from_dict(d.pop("Grading"))

        id = d.pop("ID")

        def _parse_instance_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        instance_id = _parse_instance_id(d.pop("InstanceID"))

        message = d.pop("Message")

        metadata = EntryMetadata.from_dict(d.pop("Metadata"))

        outcome = check_entry_outcome(d.pop("Outcome"))

        payload = Payload.from_dict(d.pop("Payload"))

        skip = d.pop("Skip")

        def _parse_span_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        span_id = _parse_span_id(d.pop("SpanID"))

        started_at = isoparse(d.pop("StartedAt"))

        tenant_id = d.pop("TenantID")

        def _parse_trace_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        trace_id = _parse_trace_id(d.pop("TraceID"))

        updated_at = isoparse(d.pop("UpdatedAt"))

        updated_by = d.pop("UpdatedBy")

        schema = d.pop("$schema", UNSET)

        entry = cls(
            check_id=check_id,
            config=config,
            created_at=created_at,
            created_by=created_by,
            duration_ms=duration_ms,
            evaluator_id=evaluator_id,
            findings=findings,
            finished_at=finished_at,
            grading=grading,
            id=id,
            instance_id=instance_id,
            message=message,
            metadata=metadata,
            outcome=outcome,
            payload=payload,
            skip=skip,
            span_id=span_id,
            started_at=started_at,
            tenant_id=tenant_id,
            trace_id=trace_id,
            updated_at=updated_at,
            updated_by=updated_by,
            schema=schema,
        )

        return entry
