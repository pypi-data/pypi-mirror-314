from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
import uuid

from devtools import pprint

from modelmetry.observability.finding import Finding
from modelmetry.observability.event import Event

from modelmetry.openapi import (
    Cost,
    Document,
    Money,
    Options,
    RetrievalQuery,
    Usage,
    UsageValue,
    AssistantMessage,
    SystemMessage,
    ToolMessage,
    UserMessage,
    RetrievalFamilyData,
    CompletionFamilyData,
    EmbeddingsFamilyData,
    CreateSpanParams,
    CreateSpanParamsMetadata,
    Unset,
)
from modelmetry.openapi.models.text_part import TextPart


class BaseSpan:

    def __init__(
        self,
        name: str,
        trace_id: str,
        tenant_id: str,
        parent_id: Optional[str] = None,
        message: str = "",
        severity: str = "unset",
        family: str = "other",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.xid: str = str(uuid.uuid4())
        self.tenant_id: str = tenant_id
        self.trace_id: str = trace_id
        self.parent_id: Optional[str] = parent_id
        self.name: str = name
        self.message: str = message
        self.started_at: datetime = datetime.now(timezone.utc)
        self.ended_at: Optional[datetime] = None
        self.severity: str = severity
        self.metadata: Dict[str, Any] = metadata or {}
        self.family: str = family or "other"
        self.family_data: Dict[str, Any] = {}

        self.spans: List[
            Union["CompletionSpan", "RetrievalSpan", "EmbeddingsSpan", "OtherSpan"]
        ] = []
        self.findings: List[Finding] = []
        self.events: List[Event] = []

    def finding(
        self,
        name: str,
        value: Union[float, int, bool, str],
        comment: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
    ) -> Finding:
        finding = Finding(
            name=name,
            value=value,
            tenant_id=self.tenant_id,
            trace_id=self.trace_id,
            span_id=self.xid,
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
            trace_id=self.trace_id,
            tenant_id=self.tenant_id,
            span_id=self.xid,
        )
        self.events.append(event)
        return event

    def get_events(self) -> List[Event]:
        return self.events

    def get_findings(self) -> List[Finding]:
        return self.findings

    def errored(self, error: Exception) -> None:
        self.event("errored")
        self.severity = "error"
        self.message = str(error)
        self.metadata["error"] = str(error)
        self.ended_at = datetime.now(timezone.utc)

    def completion(self, name: str) -> "CompletionSpan":
        span = CompletionSpan(
            name=name,
            trace_id=self.trace_id,
            tenant_id=self.tenant_id,
            parent_id=self.xid,
        )
        self.spans.append(span)
        return span

    def retrieval(self, name: str) -> "RetrievalSpan":
        span = RetrievalSpan(
            name=name,
            trace_id=self.trace_id,
            tenant_id=self.tenant_id,
            parent_id=self.xid,
        )
        self.spans.append(span)
        return span

    def embeddings(self, name: str) -> "EmbeddingsSpan":
        span = EmbeddingsSpan(
            name=name,
            trace_id=self.trace_id,
            tenant_id=self.tenant_id,
            parent_id=self.xid,
        )
        self.spans.append(span)
        return span

    def other_span(self, name: str) -> "OtherSpan":
        span = OtherSpan(
            name=name,
            trace_id=self.trace_id,
            tenant_id=self.tenant_id,
            parent_id=self.xid,
        )
        self.spans.append(span)
        return span

    def get_children_spans(self) -> List["BaseSpan"]:
        return self.spans

    def get_descendant_spans(self) -> List["BaseSpan"]:
        descendants = []
        for span in self.get_children_spans():
            descendants.append(span)
            descendants.extend(span.get_descendant_spans())
        return descendants

    def get_descendant_spans_count(self) -> int:
        return len(self.get_descendant_spans())

    def maybe_set_ended_at_to_now(self) -> None:
        if not self.ended_at:
            self.ended_at = datetime.now(timezone.utc)

    def set_ended_at_automatically(self):
        for span in self.get_children_spans():
            span.set_ended_at_automatically()

        if not self.ended_at:
            children_ended_at = [
                span.ended_at for span in self.get_children_spans() if span.ended_at
            ]
            if not children_ended_at:
                self.ended_at = datetime.now(timezone.utc)
                return self

            max_children_ended_at = max(children_ended_at)
            self.ended_at = max_children_ended_at

        if self.ended_at:
            children_ended_at = [
                span.ended_at for span in self.get_children_spans() if span.ended_at
            ]
            if not children_ended_at:
                return self

            max_children_ended_at = max(children_ended_at)
            if max_children_ended_at > self.ended_at:
                self.ended_at = max_children_ended_at

        return self

    def __eq__(self, other):
        if not isinstance(other, BaseSpan):
            return False
        return self.xid == other.xid

    def __hash__(self):
        return hash(self.xid)


class OtherSpan(BaseSpan):

    def __init__(
        self,
        name: str,
        trace_id: str,
        tenant_id: str,
        parent_id: Optional[str] = None,
        message: str = "",
        severity: str = "unset",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            name=name,
            trace_id=trace_id,
            tenant_id=tenant_id,
            parent_id=parent_id,
            message=message,
            severity=severity,
            family="other",
            metadata=metadata,
        )

    def to_ingest_params(self) -> CreateSpanParams:
        params = CreateSpanParams(
            xid=self.xid,
            name=self.name,
            start=self.started_at,
            end=self.ended_at or None,
            message=self.message,
            trace_id=self.trace_id,
            metadata=CreateSpanParamsMetadata.from_dict(self.metadata),
            family=self.family,
            family_data=self.family_data,
            parent_id=self.parent_id,
            severity=self.severity,
        )

        return params

    def end(self) -> "OtherSpan":
        self.maybe_set_ended_at_to_now()
        return self


class EmbeddingsSpan(BaseSpan):
    family_data: EmbeddingsFamilyData

    def __init__(
        self,
        name: str,
        trace_id: str,
        tenant_id: str,
        parent_id: Optional[str] = None,
        message: str = "",
        severity: str = "unset",
        metadata: Optional[Dict[str, Any]] = None,
        inputs: List[str] = None,
        options: Options = None,
    ):
        super().__init__(
            name=name,
            trace_id=trace_id,
            tenant_id=tenant_id,
            parent_id=parent_id,
            message=message,
            severity=severity,
            family="embeddings",
            metadata=metadata,
        )

        self.family_data = EmbeddingsFamilyData(
            inputs=inputs or [],
            options=options or Options(),
        )

    def to_ingest_params(self) -> CreateSpanParams:
        params = CreateSpanParams(
            xid=self.xid,
            name=self.name,
            start=self.started_at,
            end=self.ended_at or None,
            message=self.message,
            trace_id=self.trace_id,
            metadata=CreateSpanParamsMetadata.from_dict(self.metadata),
            family=self.family,
            family_data=self.family_data,
            parent_id=self.parent_id,
            severity=self.severity,
        )

        return params

    def end(self) -> "EmbeddingsSpan":
        self.maybe_set_ended_at_to_now()
        return self


class CompletionSpan(BaseSpan):
    family_data: CompletionFamilyData

    def __init__(
        self,
        name: str,
        trace_id: str,
        tenant_id: str,
        model: str,
        parent_id: Optional[str] = None,
        message: str = "",
        severity: str = "unset",
        metadata: Optional[Dict[str, Any]] = None,
        messages: List[
            Union[SystemMessage, UserMessage, AssistantMessage, ToolMessage]
        ] = None,
        documents: List[Document] = None,
        options: Options = None,
        usage: Usage = None,
        cost: Cost = None,
    ):
        super().__init__(
            name=name,
            trace_id=trace_id,
            tenant_id=tenant_id,
            parent_id=parent_id,
            message=message,
            severity=severity,
            family="completion",
            metadata=metadata,
        )

        self.family_data = CompletionFamilyData(
            messages=messages or [],
        )

    def end(self) -> "CompletionSpan":
        self.maybe_set_ended_at_to_now()
        return self

    def set_model(self, model: str) -> "CompletionSpan":
        self.family_data.options.model = model
        return self

    def set_provider(self, provider: str) -> "CompletionSpan":
        self.family_data.options.provider = provider
        return self

    def set_completion_messages(
        self,
        messages: List[
            Union[SystemMessage, UserMessage, AssistantMessage, ToolMessage]
        ],
    ) -> "CompletionSpan":
        self.family_data.messages = messages or []
        return

    def add_system_text(self, text: str) -> "CompletionSpan":
        self.append_message(
            SystemMessage(
                role="system",
                contents=[TextPart(text=text)],
            )
        )
        return self

    def add_user_text(self, text: str) -> "CompletionSpan":
        self.append_message(
            UserMessage(
                role="user",
                contents=[TextPart(text=text)],
            )
        )
        return self

    def add_assistant_text(self, text: str) -> "CompletionSpan":
        self.append_message(
            AssistantMessage(
                role="assistant",
                contents=[TextPart(text=text)],
            )
        )
        return self

    def append_message(
        self, message: Union[SystemMessage, UserMessage, AssistantMessage, ToolMessage]
    ) -> "CompletionSpan":
        self.family_data.messages = self.family_data.messages or []
        self.family_data.messages.append(message)
        return self

    def set_usage(
        self, kind: str, amount: int, unit: str = "tokens"
    ) -> "CompletionSpan":
        self.family_data.usage = self.family_data.usage or {}
        if kind == "input":
            self.family_data.usage.input_ = UsageValue(amount=amount, unit=unit)
        elif kind == "output":
            self.family_data.usage.output = UsageValue(amount=amount, unit=unit)
        elif kind == "total":
            self.family_data.usage.total = UsageValue(amount=amount, unit=unit)
        return self

    def set_cost(
        self, kind: str, amount: float, currency: str = "USD"
    ) -> "CompletionSpan":
        self.family_data.cost = self.family_data.cost or {}
        if kind == "input":
            self.family_data.cost.input_ = Money(amount=amount, currency=currency)
        elif kind == "output":
            self.family_data.cost.output = Money(amount=amount, currency=currency)
        elif kind == "total":
            self.family_data.cost.total = Money(amount=amount, currency=currency)
        return self

    def add_document(
        self,
        identifier: str,
        title: str,
        content_type: str,
        content: any = None,
        metadata: Dict[str, Any] = None,
    ) -> "CompletionSpan":
        self.family_data.documents = self.family_data.documents or []
        self.family_data.documents.append(
            Document(
                identifier=identifier,
                title=title,
                content_type=content_type,
                content=content or None,
                metadata=metadata or None,
            )
        )
        return self

    def to_ingest_params(self) -> CreateSpanParams:
        params = CreateSpanParams(
            xid=self.xid,
            name=self.name,
            start=self.started_at,
            end=self.ended_at or None,
            message=self.message,
            trace_id=self.trace_id,
            metadata=CreateSpanParamsMetadata.from_dict(self.metadata),
            family=self.family,
            family_data=self.family_data.to_dict(),
            parent_id=self.parent_id,
            severity=self.severity,
        )

        return params


class RetrievalSpan(BaseSpan):
    family_data: RetrievalFamilyData

    def __init__(
        self,
        name: str,
        trace_id: str,
        tenant_id: str,
        parent_id: Optional[str] = None,
        message: str = "",
        severity: str = "unset",
        metadata: Optional[Dict[str, Any]] = None,
        queries: List[RetrievalQuery] = None,
        documents: List[Document] = None,
    ):
        super().__init__(
            name=name,
            trace_id=trace_id,
            tenant_id=tenant_id,
            parent_id=parent_id,
            message=message,
            severity=severity,
            family="retrieval",
            metadata=metadata,
        )

        self.family_data = RetrievalFamilyData(
            queries=queries or [],
            documents=documents or [],
        )

    def end(self) -> "RetrievalSpan":
        self.maybe_set_ended_at_to_now()
        return self

    def add_document(
        self,
        identifier: str,
        title: str,
        content_type: str,
        content: Any = None,
        metadata: Dict[str, Any] = None,
    ) -> "RetrievalSpan":
        self.family_data.documents = self.family_data.documents or []
        self.family_data.documents.append(
            Document(
                identifier=identifier,
                title=title,
                content_type=content_type,
                content=content or None,
                metadata=metadata or None,
            )
        )
        return self

    def add_query(
        self, text_representation: str, embeddings: List[float] = None
    ) -> "RetrievalSpan":
        self.family_data.queries = self.family_data.queries or []
        self.family_data.queries.append(
            RetrievalQuery(
                text_representation=text_representation,
                embeddings=embeddings or None,
            )
        )
        return self

    def to_ingest_params(self) -> CreateSpanParams:
        params = CreateSpanParams(
            xid=self.xid,
            name=self.name,
            start=self.started_at,
            end=self.ended_at or None,
            message=self.message,
            trace_id=self.trace_id,
            metadata=CreateSpanParamsMetadata.from_dict(self.metadata),
            family=self.family,
            family_data=self.family_data,
            parent_id=self.parent_id,
            severity=self.severity,
        )

        return params
