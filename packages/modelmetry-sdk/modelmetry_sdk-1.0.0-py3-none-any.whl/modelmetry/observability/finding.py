from typing import Any, Optional, Union
from datetime import datetime, timezone
import uuid

from typing import Dict, Optional
from datetime import datetime
from modelmetry.openapi import (
    CreateFindingParams,
)
from modelmetry.openapi import (
    CreateFindingParamsMetadata,
)


class Finding:
    def __init__(
        self,
        name: str,
        value: Union[float, int, bool, str],
        tenant_id: str = None,
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
        description: Optional[str] = None,
        source: Optional[str] = "sdk",
        comment: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        at: Optional[datetime] = None,
    ) -> None:
        self.xid: str = str(uuid.uuid4())
        self.name: str = name
        self.value: Union[float, int, bool, str] = value
        self.tenant_id: str = tenant_id
        self.trace_id: Optional[str] = trace_id
        self.span_id: Optional[str] = span_id
        self.description: Optional[str] = description
        self.source: str = source or "sdk"
        self.comment: Optional[str] = comment
        self.metadata = metadata or {}
        self.at: datetime = at or datetime.now(timezone.utc)

    def set_value(self, value: Union[float, int, bool, str]) -> "Finding":
        self.value = value
        return self

    def to_ingest_params(self) -> CreateFindingParams:
        return CreateFindingParams(
            xid=self.xid,
            name=self.name,
            value=self.value,
            comment=self.comment,
            description=self.description,
            source=self.source or "sdk",
            at=self.at,
            metadata=CreateFindingParamsMetadata.from_dict(self.metadata),
            trace_id=self.trace_id,
            span_id=self.span_id,
            entry_id=None,
        )

    def __eq__(self, other):
        if not isinstance(other, Finding):
            return False
        return self.xid == other.xid

    def __hash__(self):
        return hash(self.xid)
