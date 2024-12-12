from typing import List, Union

from devtools import pprint

from modelmetry.observability.event import Event
from modelmetry.observability.finding import Finding
from modelmetry.observability.trace import Trace
from modelmetry.observability.span import (
    CompletionSpan,
    RetrievalSpan,
    EmbeddingsSpan,
    OtherSpan,
)
from modelmetry.openapi.models import (
    CreateEventParams,
    CreateFindingParams,
    CreateSpanParams,
    CreateTraceParams,
    IngestSignalsV1RequestBody,
)


def build_ingest_batch_from_traces(items: List[Trace]) -> IngestSignalsV1RequestBody:
    # ensure all traces are ended, if not just end them now
    for trace in items:
        trace.set_ended_at_automatically()

    # collect all traces, spans, events and findings
    all_traces: List[Trace] = []
    all_spans: List[Union[CompletionSpan, RetrievalSpan, EmbeddingsSpan, OtherSpan]] = (
        []
    )
    all_events: List[Event] = []
    all_findings: List[Finding] = []

    for trace in items:
        all_traces.append(trace)

        all_trace_spans = trace.get_descendant_spans()
        all_spans.extend(all_trace_spans)

        all_events.extend(trace.events)
        all_findings.extend(trace.findings)

        for span in all_trace_spans:
            all_events.extend(span.events)
            all_findings.extend(span.findings)

    # convert all to ingest params by calling on to_ingest_params on each element
    converted_traces: List[CreateTraceParams] = [
        t.to_ingest_params() for t in all_traces
    ]
    converted_spans: List[CreateSpanParams] = [s.to_ingest_params() for s in all_spans]
    converted_events: List[CreateEventParams] = [
        e.to_ingest_params() for e in all_events
    ]
    converted_findings: List[CreateFindingParams] = [
        f.to_ingest_params() for f in all_findings
    ]

    body = IngestSignalsV1RequestBody(
        traces=converted_traces,
        spans=converted_spans,
        events=converted_events,
        findings=converted_findings,
    )

    return body
