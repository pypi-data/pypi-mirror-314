import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.trace_metadata import TraceMetadata


T = TypeVar("T", bound="Trace")


@_attrs_define
class Trace:
    """
    Attributes:
        created_at (datetime.datetime):
        end (datetime.datetime):
        id (str):
        metadata (TraceMetadata):
        name (str):
        start (datetime.datetime):
        tenant_id (str):
        updated_at (datetime.datetime):
        xid (str):
        session_id (Union[None, Unset, str]):
    """

    created_at: datetime.datetime
    end: datetime.datetime
    id: str
    metadata: "TraceMetadata"
    name: str
    start: datetime.datetime
    tenant_id: str
    updated_at: datetime.datetime
    xid: str
    session_id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        end = self.end.isoformat()

        id = self.id

        metadata = self.metadata.to_dict()

        name = self.name

        start = self.start.isoformat()

        tenant_id = self.tenant_id

        updated_at = self.updated_at.isoformat()

        xid = self.xid

        session_id: Union[None, Unset, str]
        if isinstance(self.session_id, Unset):
            session_id = UNSET
        else:
            session_id = self.session_id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "CreatedAt": created_at,
                "End": end,
                "ID": id,
                "Metadata": metadata,
                "Name": name,
                "Start": start,
                "TenantID": tenant_id,
                "UpdatedAt": updated_at,
                "XID": xid,
            }
        )
        if session_id is not UNSET:
            field_dict["SessionID"] = session_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.trace_metadata import TraceMetadata

        d = src_dict.copy()
        created_at = isoparse(d.pop("CreatedAt"))

        end = isoparse(d.pop("End"))

        id = d.pop("ID")

        metadata = TraceMetadata.from_dict(d.pop("Metadata"))

        name = d.pop("Name")

        start = isoparse(d.pop("Start"))

        tenant_id = d.pop("TenantID")

        updated_at = isoparse(d.pop("UpdatedAt"))

        xid = d.pop("XID")

        def _parse_session_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        session_id = _parse_session_id(d.pop("SessionID", UNSET))

        trace = cls(
            created_at=created_at,
            end=end,
            id=id,
            metadata=metadata,
            name=name,
            start=start,
            tenant_id=tenant_id,
            updated_at=updated_at,
            xid=xid,
            session_id=session_id,
        )

        return trace
