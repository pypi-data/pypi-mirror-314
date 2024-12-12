import unittest
from modelmetry.observability.span import (
    EmbeddingsSpan,
    CompletionSpan,
    RetrievalSpan,
    OtherSpan,
)


class TestSpan(unittest.TestCase):

    def test_maybe_set_ended_at_to_now(self):
        span = EmbeddingsSpan(name="span", tenant_id="ten_test", trace_id="tra_test")
        self.assertIsNone(span.ended_at)
        span.maybe_set_ended_at_to_now()
        self.assertIsNotNone(span.ended_at)

    def test_set_ended_at_automatically(self):
        span = EmbeddingsSpan(name="span", tenant_id="ten_test", trace_id="tra_test")
        span1 = span.other_span(name="span1")
        span1_1 = span1.other_span(name="span1_1")
        span1_1.maybe_set_ended_at_to_now()
        span1_1_1 = span1_1.other_span(name="span1_1_1")
        span1_1_1.maybe_set_ended_at_to_now()
        span1_2 = span1.other_span(name="span1_2")
        span1_2.maybe_set_ended_at_to_now()
        span.set_ended_at_automatically()
        self.assertIsNotNone(span.ended_at)
        self.assertIsNotNone(span1.ended_at)
        self.assertIsNotNone(span1_1.ended_at)
        self.assertIsNotNone(span1_1_1.ended_at)
        self.assertIsNotNone(span1_2.ended_at)
        self.assertGreaterEqual(span.ended_at, span1.ended_at)
        self.assertGreaterEqual(span1.ended_at, span1_1.ended_at)
        self.assertGreaterEqual(span1.ended_at, span1_1_1.ended_at)
        self.assertGreaterEqual(span1.ended_at, span1_2.ended_at)

    def test_get_children_spans(self):
        span = RetrievalSpan(name="span", tenant_id="ten_test", trace_id="tra_test")
        span1 = span.other_span(name="span1")
        span2 = span.other_span(name="span2")
        children = span.get_children_spans()
        self.assertIn(span1, children)
        self.assertIn(span2, children)
        self.assertEqual(len(children), 2)

    def test_get_descendant_spans(self):
        span1 = OtherSpan(name="span1", tenant_id="ten_test", trace_id="tra_test")
        span1_1 = span1.other_span(name="span1_1")
        span1_1_1 = span1_1.other_span(name="span1_1_1")
        span1_2 = span1.other_span(name="span1_2")
        descendants = span1.get_descendant_spans()
        count = span1.get_descendant_spans_count()
        self.assertIn(span1_1, descendants)
        self.assertIn(span1_1_1, descendants)
        self.assertIn(span1_2, descendants)
        self.assertEqual(len(descendants), 3)
        self.assertEqual(count, 3)

    def test_to_ingest_params(self):
        span = CompletionSpan(
            name="span",
            tenant_id="ten_test",
            trace_id="tra_test",
            model="openai/gpt-3.5-turbo",
        )
        span.maybe_set_ended_at_to_now()

        params = span.to_ingest_params()
        self.assertEqual(params.xid, span.xid)
        self.assertEqual(params.name, span.name)
        self.assertEqual(params.trace_id, span.trace_id)
        self.assertEqual(params.parent_id, span.parent_id)
        self.assertEqual(params.start, span.started_at)
        self.assertEqual(params.end, span.ended_at)
        self.assertEqual(params.metadata, span.metadata)
        self.assertEqual(params.family, span.family)
        self.assertEqual(params.family_data, span.family_data)
        self.assertEqual(params.message, span.message)
        self.assertEqual(params.severity, span.severity)
