import unittest
from datetime import datetime
from modelmetry.observability.trace import Trace
from modelmetry.observability.span import (
    EmbeddingsSpan,
    CompletionSpan,
    RetrievalSpan,
    OtherSpan,
)


class TestTrace(unittest.TestCase):
    def test_constructor(self):
        # test initializing a Trace object with arguements
        trace = Trace(name="test", tenant_id="tenant_id")
        self.assertEqual(trace.name, "test")
        self.assertEqual(trace.tenant_id, "tenant_id")
        self.assertEqual(trace.metadata, {})
        self.assertIsInstance(trace.started_at, datetime)

        # add metadata
        trace = Trace(name="test", tenant_id="tenant_id", metadata={"key": "value"})
        self.assertEqual(trace.metadata, {"key": "value"})

        # update metadata
        trace.metadata["foo"] = 4.4
        self.assertEqual(trace.metadata, {"key": "value", "foo": 4.4})

    def test_create_a_span_with_family(self):
        # test creating concrate spans: CompletionSpan, RetrievalSpan, EmbeddingsSpan, OtherSpan.

        # test completion span
        trace = Trace(name="test", tenant_id="tenant_id")
        completion_span = trace.completion(
            name="test_completion", model="openai/gpt-3.5-turbo"
        )
        self.assertIsInstance(completion_span, CompletionSpan)
        self.assertEqual(completion_span.name, "test_completion")
        self.assertEqual(completion_span.trace_id, trace.xid)

        # test retrieval span
        trace = Trace(name="test", tenant_id="tenant_id")
        retrieval_span = trace.retrieval(name="test_retrieval")
        self.assertIsInstance(retrieval_span, RetrievalSpan)
        self.assertEqual(retrieval_span.name, "test_retrieval")
        self.assertEqual(retrieval_span.trace_id, trace.xid)

        # test embeddings span
        trace = Trace(name="test", tenant_id="tenant_id")
        embeddings_span = trace.embeddings(name="test_embeddings")
        self.assertIsInstance(embeddings_span, EmbeddingsSpan)
        self.assertEqual(embeddings_span.name, "test_embeddings")
        self.assertEqual(embeddings_span.trace_id, trace.xid)

        # test other span
        trace = Trace(name="test", tenant_id="tenant_id")
        other_span = trace.other_span(name="test_other")
        self.assertIsInstance(other_span, OtherSpan)
        self.assertEqual(other_span.name, "test_other")
        self.assertEqual(other_span.trace_id, trace.xid)

    def test_returns_all_descendant_spans(self):
        # test the method that returns all descendant spans of a given span, even with deeply nested spans.
        trace = Trace(name="test", tenant_id="tenant_id")
        span1 = trace.other_span("span1")
        span1_1 = span1.other_span("span1_1")
        span1_2 = span1.other_span("span1_2")
        span1_2_1 = span1_2.other_span("span1_2_1")
        span1_2_1_1 = span1_2_1.other_span("span1_2_1_1")
        span1_2_2 = span1_2.other_span("span1_2_2")
        span2 = trace.other_span("span2")
        span3 = span1.other_span("span3")

        descendant_spans = trace.get_descendant_spans()
        self.assertEqual(len(descendant_spans), 8)
        self.assertIn(span1, descendant_spans)
        self.assertIn(span1_1, descendant_spans)
        self.assertIn(span1_2, descendant_spans)
        self.assertIn(span1_2_1, descendant_spans)
        self.assertIn(span1_2_1_1, descendant_spans)
        self.assertIn(span1_2_2, descendant_spans)
        self.assertIn(span2, descendant_spans)
        self.assertIn(span3, descendant_spans)

    def test_to_ingest_params(self):
        # test to_ingest_params method and ensure it returns the correct CreateTraceParams object with the correct values
        trace = Trace(
            name="test",
            tenant_id="tenant_id",
            metadata={"key": "value", "foo": 4.4, "bar": False},
        )
        span1 = trace.other_span("span1")
        span1_1 = span1.other_span("span1_1")
        span1_1_1 = span1_1.other_span("span1_1_1")
        span2 = trace.other_span("span2")
        trace.end()

        ingest_params = trace.to_ingest_params()
        self.assertEqual(ingest_params.xid, trace.xid)
        self.assertEqual(ingest_params.name, trace.name)
        self.assertEqual(ingest_params.metadata, trace.metadata)
        self.assertEqual(ingest_params.start, trace.started_at)
        self.assertEqual(ingest_params.end, trace.ended_at)
        self.assertIsNone(ingest_params.session_id)

    def test_setting_ended_at_automatically_when_there_are_child_spans(self):
        # test setting endedAt automatically when there are child spans
        trace = Trace(name="test", tenant_id="ten_test")
        span1 = trace.other_span(name="span1")
        span2 = trace.other_span(name="span2")
        span1.ended_at = datetime(2022, 1, 1)
        span2.ended_at = datetime(2022, 1, 2)
        trace.set_ended_at_automatically()
        self.assertEqual(trace.ended_at, datetime(2022, 1, 2))
