from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.summarised_entry_outcome import SummarisedEntryOutcome, check_summarised_entry_outcome

if TYPE_CHECKING:
    from ..models.simplified_finding import SimplifiedFinding


T = TypeVar("T", bound="SummarisedEntry")


@_attrs_define
class SummarisedEntry:
    """
    Attributes:
        check_id (Union[None, str]):
        duration_ms (int):
        evaluator_id (str):
        findings (Union[None, list['SimplifiedFinding']]):
        id (str):
        instance_id (Union[None, str]):
        message (str):
        outcome (SummarisedEntryOutcome): The status of the entry. Default: 'na'.
        skip (str):
        span_id (Union[None, str]):
        tenant_id (str):
        trace_id (Union[None, str]):
    """

    check_id: Union[None, str]
    duration_ms: int
    evaluator_id: str
    findings: Union[None, list["SimplifiedFinding"]]
    id: str
    instance_id: Union[None, str]
    message: str
    skip: str
    span_id: Union[None, str]
    tenant_id: str
    trace_id: Union[None, str]
    outcome: SummarisedEntryOutcome = "na"

    def to_dict(self) -> dict[str, Any]:
        check_id: Union[None, str]
        check_id = self.check_id

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

        id = self.id

        instance_id: Union[None, str]
        instance_id = self.instance_id

        message = self.message

        outcome: str = self.outcome

        skip = self.skip

        span_id: Union[None, str]
        span_id = self.span_id

        tenant_id = self.tenant_id

        trace_id: Union[None, str]
        trace_id = self.trace_id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "CheckID": check_id,
                "DurationMs": duration_ms,
                "EvaluatorID": evaluator_id,
                "Findings": findings,
                "ID": id,
                "InstanceID": instance_id,
                "Message": message,
                "Outcome": outcome,
                "Skip": skip,
                "SpanID": span_id,
                "TenantID": tenant_id,
                "TraceID": trace_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.simplified_finding import SimplifiedFinding

        d = src_dict.copy()

        def _parse_check_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        check_id = _parse_check_id(d.pop("CheckID"))

        duration_ms = d.pop("DurationMs")

        evaluator_id = d.pop("EvaluatorID")

        def _parse_findings(data: object) -> Union[None, list["SimplifiedFinding"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                findings_type_0 = []
                _findings_type_0 = data
                for findings_type_0_item_data in _findings_type_0:
                    findings_type_0_item = SimplifiedFinding.from_dict(findings_type_0_item_data)

                    findings_type_0.append(findings_type_0_item)

                return findings_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["SimplifiedFinding"]], data)

        findings = _parse_findings(d.pop("Findings"))

        id = d.pop("ID")

        def _parse_instance_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        instance_id = _parse_instance_id(d.pop("InstanceID"))

        message = d.pop("Message")

        outcome = check_summarised_entry_outcome(d.pop("Outcome"))

        skip = d.pop("Skip")

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

        summarised_entry = cls(
            check_id=check_id,
            duration_ms=duration_ms,
            evaluator_id=evaluator_id,
            findings=findings,
            id=id,
            instance_id=instance_id,
            message=message,
            outcome=outcome,
            skip=skip,
            span_id=span_id,
            tenant_id=tenant_id,
            trace_id=trace_id,
        )

        return summarised_entry
