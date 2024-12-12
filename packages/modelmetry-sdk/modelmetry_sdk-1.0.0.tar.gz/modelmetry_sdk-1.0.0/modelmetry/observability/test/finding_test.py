import unittest

import unittest
from datetime import datetime, timezone
from modelmetry.observability.finding import Finding


class TestFinding(unittest.TestCase):
    def test_constructor(self):
        name = "test_name"
        value = 42
        trace_id = "test_trace_id"
        span_id = "test_span_id"
        description = "test_description"
        source = "sdk"
        comment = "test_comment"
        metadata = {"key1": "value1", "key2": "value2"}
        at = datetime.now(timezone.utc)

        finding = Finding(
            name=name,
            value=value,
            trace_id=trace_id,
            span_id=span_id,
            description=description,
            source=source,
            comment=comment,
            metadata=metadata,
            at=at,
        )

        self.assertEqual(finding.name, name)
        self.assertEqual(finding.value, value)
        self.assertEqual(finding.trace_id, trace_id)
        self.assertEqual(finding.span_id, span_id)
        self.assertEqual(finding.description, description)
        self.assertEqual(finding.source, source)
        self.assertEqual(finding.comment, comment)
        self.assertEqual(finding.metadata, metadata)
        self.assertEqual(finding.at, at)

    def test_to_ingest_params(self):
        name = "test_name"
        value = 42
        trace_id = "test_trace_id"
        span_id = "test_span_id"
        description = "test_description"
        source = "sdk"
        comment = "test_comment"
        metadata = {"key1": "value1", "key2": "value2"}
        at = datetime.now(timezone.utc)

        finding = Finding(
            name=name,
            value=value,
            trace_id=trace_id,
            span_id=span_id,
            description=description,
            source=source,
            comment=comment,
            metadata=metadata,
            at=at,
        )

        ingest_params = finding.to_ingest_params()

        self.assertEqual(ingest_params.xid, finding.xid)
        self.assertEqual(ingest_params.name, finding.name)
        self.assertEqual(ingest_params.value, finding.value)
        self.assertEqual(ingest_params.comment, finding.comment)
        self.assertEqual(ingest_params.description, finding.description)
        self.assertEqual(ingest_params.source, finding.source)
        self.assertEqual(ingest_params.at, finding.at)
        self.assertEqual(ingest_params.metadata, finding.metadata)
        self.assertEqual(ingest_params.trace_id, finding.trace_id)
        self.assertEqual(ingest_params.span_id, finding.span_id)
        self.assertEqual(ingest_params.entry_id, None)
