from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
import uuid

from modelmetry.observability.event import Event
from modelmetry.observability.finding import Finding
from modelmetry.observability.span import (
    CompletionSpan,
    EmbeddingsSpan,
    OtherSpan,
    RetrievalSpan,
)
from modelmetry.openapi import (
    CreateTraceParams,
    CreateTraceParamsMetadata,
)


class Trace:

    spans: List[Union[CompletionSpan, RetrievalSpan, EmbeddingsSpan, OtherSpan]] = []

    def __init__(self, name: str, tenant_id: str, metadata: Dict[str, Any] = None):
        self.xid = str(uuid.uuid4())
        self.tenant_id = tenant_id
        self.name = name
        self.metadata = metadata or {}
        self.started_at = datetime.now(timezone.utc)
        self.ended_at = None

        self.spans = []
        self.events = []
        self.findings = []

    # create new signals

    def completion(self, name: str, model: str) -> CompletionSpan:
        span = CompletionSpan(
            name=name,
            trace_id=self.xid,
            tenant_id=self.tenant_id,
            model=model,
        )
        self.spans.append(span)
        return span

    def retrieval(self, name: str) -> RetrievalSpan:
        span = RetrievalSpan(
            name=name,
            trace_id=self.xid,
            tenant_id=self.tenant_id,
        )
        self.spans.append(span)
        return span

    def embeddings(self, name: str) -> EmbeddingsSpan:
        span = EmbeddingsSpan(
            name=name,
            trace_id=self.xid,
            tenant_id=self.tenant_id,
        )
        self.spans.append(span)
        return span

    def other_span(self, name: str) -> OtherSpan:
        span = OtherSpan(
            name=name,
            trace_id=self.xid,
            tenant_id=self.tenant_id,
        )
        self.spans.append(span)
        return span

    def finding(
        self,
        name: str,
        value: Union[int, bool, str],
        comment: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
    ) -> Finding:
        finding = Finding(
            name=name,
            value=value,
            trace_id=self.xid,
            span_id=None,
            comment=comment,
            description=description,
            metadata=metadata,
            source=source,
        )
        self.findings.append(finding)
        return finding

    def event(self, name: str) -> Event:
        event = Event(
            name=name,
            trace_id=self.xid,
            span_id=None,
        )
        self.events.append(event)
        return event

    # behaviour

    def end(self) -> "Trace":
        if not self.ended_at:
            self.ended_at = datetime.now(timezone.utc)
        return self

    def set_ended_at_automatically(self) -> "Trace":
        for span in self.get_children_spans():
            span.set_ended_at_automatically()

        if not self.ended_at:
            children_ended_at = [span.ended_at for span in self.get_children_spans()]
            children_ended_at = [date for date in children_ended_at if date]

            if not children_ended_at:
                self.ended_at = datetime.now(timezone.utc)
                return self

            max_children_ended_at = max(children_ended_at)
            self.ended_at = max_children_ended_at

        return self

    def get_children_spans(
        self,
    ) -> List[Union[CompletionSpan, RetrievalSpan, EmbeddingsSpan, OtherSpan]]:
        return self.spans

    def get_descendant_spans(
        self,
    ) -> List[Union[CompletionSpan, RetrievalSpan, EmbeddingsSpan, OtherSpan]]:
        descendant_spans = []
        for span in self.spans:
            descendant_spans.append(span)
            descendant_spans.extend(span.get_descendant_spans())
        return descendant_spans

    def get_duration_in_milliseconds(self) -> int:
        if not self.ended_at:
            return 0
        return (self.ended_at - self.started_at).total_seconds() * 1000

    def get_descendant_spans_count(self) -> int:
        return len(self.get_descendant_spans())

    def get_events(self) -> List[Event]:
        return self.events

    def get_findings(self) -> List[Finding]:
        return self.findings

    def to_ingest_params(self) -> CreateTraceParams:
        return CreateTraceParams(
            xid=self.xid,
            name=self.name,
            start=self.started_at,
            end=self.ended_at or None,
            metadata=CreateTraceParamsMetadata.from_dict(self.metadata),
            session_id=None,
        )

    def has_ended(self) -> bool:
        return bool(self.ended_at)

    def __eq__(self, other):
        if not isinstance(other, Trace):
            return False
        return self.xid == other.xid

    def __hash__(self):
        return hash(self.xid)
