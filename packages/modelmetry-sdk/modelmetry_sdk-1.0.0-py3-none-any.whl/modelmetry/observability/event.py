import sys

sys.path.append(".")

import uuid

from typing import Any, Dict, Optional
from datetime import datetime, timezone
from modelmetry.openapi import (
    CreateEventParams,
    CreateEventParamsMetadata,
)


class Event:
    def __init__(
        self,
        name: str,
        tenant_id: str = None,
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
        at: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.xid = str(uuid.uuid4())
        self.name = name
        self.trace_id = trace_id
        self.tenant_id = tenant_id
        self.span_id = span_id
        self.at = at or datetime.now(timezone.utc)
        self.metadata = metadata or {}

    def to_ingest_params(self) -> CreateEventParams:
        return CreateEventParams(
            xid=self.xid,
            name=self.name,
            at=self.at,
            metadata=CreateEventParamsMetadata.from_dict(self.metadata),
            trace_id=self.trace_id,
            span_id=self.span_id,
            entry_id=None,
        )

    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        return self.xid == other.xid

    def __hash__(self):
        return hash(self.xid)
