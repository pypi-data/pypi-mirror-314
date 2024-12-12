import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_trace_params_metadata import CreateTraceParamsMetadata


T = TypeVar("T", bound="CreateTraceParams")


@_attrs_define
class CreateTraceParams:
    """
    Attributes:
        start (datetime.datetime):
        xid (str):
        end (Union[None, Unset, datetime.datetime]):
        metadata (Union[Unset, CreateTraceParamsMetadata]):
        name (Union[None, Unset, str]):
        session_id (Union[None, Unset, str]):
    """

    start: datetime.datetime
    xid: str
    end: Union[None, Unset, datetime.datetime] = UNSET
    metadata: Union[Unset, "CreateTraceParamsMetadata"] = UNSET
    name: Union[None, Unset, str] = UNSET
    session_id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        start = self.start.isoformat()

        xid = self.xid

        end: Union[None, Unset, str]
        if isinstance(self.end, Unset):
            end = UNSET
        elif isinstance(self.end, datetime.datetime):
            end = self.end.isoformat()
        else:
            end = self.end

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        session_id: Union[None, Unset, str]
        if isinstance(self.session_id, Unset):
            session_id = UNSET
        else:
            session_id = self.session_id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Start": start,
                "XID": xid,
            }
        )
        if end is not UNSET:
            field_dict["End"] = end
        if metadata is not UNSET:
            field_dict["Metadata"] = metadata
        if name is not UNSET:
            field_dict["Name"] = name
        if session_id is not UNSET:
            field_dict["SessionID"] = session_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_trace_params_metadata import CreateTraceParamsMetadata

        d = src_dict.copy()
        start = isoparse(d.pop("Start"))

        xid = d.pop("XID")

        def _parse_end(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_type_0 = isoparse(data)

                return end_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        end = _parse_end(d.pop("End", UNSET))

        _metadata = d.pop("Metadata", UNSET)
        metadata: Union[Unset, CreateTraceParamsMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreateTraceParamsMetadata.from_dict(_metadata)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("Name", UNSET))

        def _parse_session_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        session_id = _parse_session_id(d.pop("SessionID", UNSET))

        create_trace_params = cls(
            start=start,
            xid=xid,
            end=end,
            metadata=(
                CreateTraceParamsMetadata.from_dict(metadata)
                if not isinstance(metadata, Unset)
                else UNSET
            ),
            name=name,
            session_id=session_id,
        )

        return create_trace_params
