from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_event_params import CreateEventParams
    from ..models.create_finding_params import CreateFindingParams
    from ..models.create_session_params import CreateSessionParams
    from ..models.create_span_params import CreateSpanParams
    from ..models.create_trace_params import CreateTraceParams


T = TypeVar("T", bound="IngestSignalsV1RequestBody")


@_attrs_define
class IngestSignalsV1RequestBody:
    """
    Attributes:
        schema (Union[Unset, str]): A URL to the JSON Schema for this object.
        events (Union[None, Unset, list['CreateEventParams']]):
        findings (Union[None, Unset, list['CreateFindingParams']]):
        sessions (Union[None, Unset, list['CreateSessionParams']]):
        spans (Union[None, Unset, list['CreateSpanParams']]):
        traces (Union[None, Unset, list['CreateTraceParams']]):
    """

    schema: Union[Unset, str] = UNSET
    events: Union[None, Unset, list["CreateEventParams"]] = UNSET
    findings: Union[None, Unset, list["CreateFindingParams"]] = UNSET
    sessions: Union[None, Unset, list["CreateSessionParams"]] = UNSET
    spans: Union[None, Unset, list["CreateSpanParams"]] = UNSET
    traces: Union[None, Unset, list["CreateTraceParams"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        events: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.events, Unset):
            events = UNSET
        elif isinstance(self.events, list):
            events = []
            for events_type_0_item_data in self.events:
                events_type_0_item = events_type_0_item_data.to_dict()
                events.append(events_type_0_item)

        else:
            events = self.events

        findings: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.findings, Unset):
            findings = UNSET
        elif isinstance(self.findings, list):
            findings = []
            for findings_type_0_item_data in self.findings:
                findings_type_0_item = findings_type_0_item_data.to_dict()
                findings.append(findings_type_0_item)

        else:
            findings = self.findings

        sessions: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.sessions, Unset):
            sessions = UNSET
        elif isinstance(self.sessions, list):
            sessions = []
            for sessions_type_0_item_data in self.sessions:
                sessions_type_0_item = sessions_type_0_item_data.to_dict()
                sessions.append(sessions_type_0_item)

        else:
            sessions = self.sessions

        spans: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.spans, Unset):
            spans = UNSET
        elif isinstance(self.spans, list):
            spans = []
            for spans_type_0_item_data in self.spans:
                spans_type_0_item = spans_type_0_item_data.to_dict()
                spans.append(spans_type_0_item)

        else:
            spans = self.spans

        traces: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.traces, Unset):
            traces = UNSET
        elif isinstance(self.traces, list):
            traces = []
            for traces_type_0_item_data in self.traces:
                traces_type_0_item = traces_type_0_item_data.to_dict()
                traces.append(traces_type_0_item)

        else:
            traces = self.traces

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if events is not UNSET:
            field_dict["Events"] = events
        if findings is not UNSET:
            field_dict["Findings"] = findings
        if sessions is not UNSET:
            field_dict["Sessions"] = sessions
        if spans is not UNSET:
            field_dict["Spans"] = spans
        if traces is not UNSET:
            field_dict["Traces"] = traces

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_event_params import CreateEventParams
        from ..models.create_finding_params import CreateFindingParams
        from ..models.create_session_params import CreateSessionParams
        from ..models.create_span_params import CreateSpanParams
        from ..models.create_trace_params import CreateTraceParams

        d = src_dict.copy()
        schema = d.pop("$schema", UNSET)

        def _parse_events(data: object) -> Union[None, Unset, list["CreateEventParams"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                events_type_0 = []
                _events_type_0 = data
                for events_type_0_item_data in _events_type_0:
                    events_type_0_item = CreateEventParams.from_dict(events_type_0_item_data)

                    events_type_0.append(events_type_0_item)

                return events_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CreateEventParams"]], data)

        events = _parse_events(d.pop("Events", UNSET))

        def _parse_findings(data: object) -> Union[None, Unset, list["CreateFindingParams"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                findings_type_0 = []
                _findings_type_0 = data
                for findings_type_0_item_data in _findings_type_0:
                    findings_type_0_item = CreateFindingParams.from_dict(findings_type_0_item_data)

                    findings_type_0.append(findings_type_0_item)

                return findings_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CreateFindingParams"]], data)

        findings = _parse_findings(d.pop("Findings", UNSET))

        def _parse_sessions(data: object) -> Union[None, Unset, list["CreateSessionParams"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sessions_type_0 = []
                _sessions_type_0 = data
                for sessions_type_0_item_data in _sessions_type_0:
                    sessions_type_0_item = CreateSessionParams.from_dict(sessions_type_0_item_data)

                    sessions_type_0.append(sessions_type_0_item)

                return sessions_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CreateSessionParams"]], data)

        sessions = _parse_sessions(d.pop("Sessions", UNSET))

        def _parse_spans(data: object) -> Union[None, Unset, list["CreateSpanParams"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                spans_type_0 = []
                _spans_type_0 = data
                for spans_type_0_item_data in _spans_type_0:
                    spans_type_0_item = CreateSpanParams.from_dict(spans_type_0_item_data)

                    spans_type_0.append(spans_type_0_item)

                return spans_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CreateSpanParams"]], data)

        spans = _parse_spans(d.pop("Spans", UNSET))

        def _parse_traces(data: object) -> Union[None, Unset, list["CreateTraceParams"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                traces_type_0 = []
                _traces_type_0 = data
                for traces_type_0_item_data in _traces_type_0:
                    traces_type_0_item = CreateTraceParams.from_dict(traces_type_0_item_data)

                    traces_type_0.append(traces_type_0_item)

                return traces_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CreateTraceParams"]], data)

        traces = _parse_traces(d.pop("Traces", UNSET))

        ingest_signals_v1_request_body = cls(
            schema=schema,
            events=events,
            findings=findings,
            sessions=sessions,
            spans=spans,
            traces=traces,
        )

        return ingest_signals_v1_request_body
