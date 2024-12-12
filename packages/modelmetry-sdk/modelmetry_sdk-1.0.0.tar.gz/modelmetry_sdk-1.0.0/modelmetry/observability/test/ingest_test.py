import unittest
from datetime import datetime
from modelmetry.observability.ingest import build_ingest_batch_from_traces
from modelmetry.observability.span import (
    EmbeddingsSpan,
    CompletionSpan,
    RetrievalSpan,
    OtherSpan,
)
from modelmetry.observability.trace import Trace


class TestIngest(unittest.TestCase):

    def test_build_ingest_batch_from_traces(self):

        trace1 = Trace(name="trace1", tenant_id="ten_test", metadata={"a": 1})
        trace2 = Trace(name="trace2", tenant_id="ten_test", metadata={"a": 2})
        trace3 = Trace(name="trace3", tenant_id="ten_test", metadata={"a": 3})

        trace1_span1 = trace2.completion(name="trace1.span1", model="model1")
        trace1_span1_event1 = trace1_span1.event(name="trace1.span1.event1")
        trace1_span1_1 = trace1_span1.retrieval(name="trace1.span1_1")
        trace1_finding1 = trace1.finding(
            name="trace1.finding1", value=5, comment="cmt1"
        )

        trace2_span1 = trace2.completion(name="trace2.span1", model="model2")
        trace2_span1.add_system_text("system text")
        trace2_span1.add_user_text("user text")
        trace2_span1.add_assistant_text("assistant text")

        trace2_span1_event1 = trace2_span1.event(name="trace2.span1.event1")
        trace2_span1_finding1 = trace2_span1.finding(
            name="trace2.span1.finding1", value=6, comment="cmt2"
        )

        traces = [trace1, trace2, trace3]
        batch = build_ingest_batch_from_traces(traces)

        self.assertEqual(len(batch.traces), 3)
        self.assertEqual(len(batch.spans), 3)
        self.assertEqual(len(batch.events), 2)
        self.assertEqual(len(batch.findings), 2)

        self.assertIn(trace1.to_ingest_params(), batch.traces)
        self.assertIn(trace2.to_ingest_params(), batch.traces)
        self.assertIn(trace3.to_ingest_params(), batch.traces)

        self.assertIn(trace1_span1.to_ingest_params(), batch.spans)
        self.assertIn(trace1_span1_1.to_ingest_params(), batch.spans)
        self.assertIn(trace2_span1.to_ingest_params(), batch.spans)

        self.assertIn(trace1_span1_event1.to_ingest_params(), batch.events)
        self.assertIn(trace2_span1_event1.to_ingest_params(), batch.events)

        self.assertIn(trace1_finding1.to_ingest_params(), batch.findings)
        self.assertIn(trace2_span1_finding1.to_ingest_params(), batch.findings)
