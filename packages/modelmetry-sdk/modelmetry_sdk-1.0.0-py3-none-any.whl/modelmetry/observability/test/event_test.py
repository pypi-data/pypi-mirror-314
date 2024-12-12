import unittest

import unittest
from datetime import datetime, timezone
from modelmetry.observability.event import Event


class TestEvent(unittest.TestCase):
    def test_constructor(self):
        name = "test_event"
        trace_id = "12345"
        span_id = "67890"
        at = datetime.now(timezone.utc)
        metadata = {"key1": "value1", "key2": "value2"}

        event = Event(
            name=name, trace_id=trace_id, span_id=span_id, at=at, metadata=metadata
        )

        self.assertEqual(event.name, name)
        self.assertEqual(event.trace_id, trace_id)
        self.assertEqual(event.span_id, span_id)
        self.assertEqual(event.at, at)
        self.assertEqual(event.metadata, metadata)

    def test_to_ingest_params(self):
        name = "test_event"
        trace_id = "12345"
        span_id = "67890"
        at = datetime.now(timezone.utc)
        metadata = {"key1": "value1", "key2": "value2"}

        event = Event(
            name=name, trace_id=trace_id, span_id=span_id, at=at, metadata=metadata
        )
        ingest_params = event.to_ingest_params()

        self.assertEqual(ingest_params.xid, event.xid)
        self.assertEqual(ingest_params.name, event.name)
        self.assertEqual(ingest_params.at, event.at)
        self.assertEqual(ingest_params.metadata.to_dict(), event.metadata)
        self.assertEqual(ingest_params.trace_id, event.trace_id)
        self.assertEqual(ingest_params.span_id, event.span_id)
        self.assertIsNone(ingest_params.entry_id)
