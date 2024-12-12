import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_span_params_metadata import CreateSpanParamsMetadata


T = TypeVar("T", bound="CreateSpanParams")


@_attrs_define
class CreateSpanParams:
    """
    Attributes:
        end (Union[None, datetime.datetime]):
        name (str):
        start (datetime.datetime):
        trace_id (str):
        xid (str):
        family (Union[None, Unset, str]):
        family_data (Union[Unset, Any]):
        message (Union[None, Unset, str]):
        metadata (Union[Unset, CreateSpanParamsMetadata]):
        parent_id (Union[None, Unset, str]):
        severity (Union[None, Unset, str]):
    """

    end: Union[None, datetime.datetime]
    name: str
    start: datetime.datetime
    trace_id: str
    xid: str
    family: Union[None, Unset, str] = UNSET
    family_data: Union[Unset, Any] = UNSET
    message: Union[None, Unset, str] = UNSET
    metadata: Union[Unset, "CreateSpanParamsMetadata"] = UNSET
    parent_id: Union[None, Unset, str] = UNSET
    severity: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        end: Union[None, str]
        if isinstance(self.end, datetime.datetime):
            end = self.end.isoformat()
        else:
            end = self.end

        name = self.name

        start = self.start.isoformat()

        trace_id = self.trace_id

        xid = self.xid

        family: Union[None, Unset, str]
        if isinstance(self.family, Unset):
            family = UNSET
        else:
            family = self.family

        family_data = self.family_data

        message: Union[None, Unset, str]
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        parent_id: Union[None, Unset, str]
        if isinstance(self.parent_id, Unset):
            parent_id = UNSET
        else:
            parent_id = self.parent_id

        severity: Union[None, Unset, str]
        if isinstance(self.severity, Unset):
            severity = UNSET
        else:
            severity = self.severity

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "End": end,
                "Name": name,
                "Start": start,
                "TraceID": trace_id,
                "XID": xid,
            }
        )
        if family is not UNSET:
            field_dict["Family"] = family
        if family_data is not UNSET:
            field_dict["FamilyData"] = family_data
        if message is not UNSET:
            field_dict["Message"] = message
        if metadata is not UNSET:
            field_dict["Metadata"] = metadata
        if parent_id is not UNSET:
            field_dict["ParentID"] = parent_id
        if severity is not UNSET:
            field_dict["Severity"] = severity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_span_params_metadata import CreateSpanParamsMetadata

        d = src_dict.copy()

        def _parse_end(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_type_0 = isoparse(data)

                return end_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        end = _parse_end(d.pop("End"))

        name = d.pop("Name")

        start = isoparse(d.pop("Start"))

        trace_id = d.pop("TraceID")

        xid = d.pop("XID")

        def _parse_family(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        family = _parse_family(d.pop("Family", UNSET))

        family_data = d.pop("FamilyData", UNSET)

        def _parse_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        message = _parse_message(d.pop("Message", UNSET))

        _metadata = d.pop("Metadata", UNSET)
        metadata: Union[Unset, CreateSpanParamsMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreateSpanParamsMetadata.from_dict(_metadata)

        def _parse_parent_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parent_id = _parse_parent_id(d.pop("ParentID", UNSET))

        def _parse_severity(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        severity = _parse_severity(d.pop("Severity", UNSET))

        create_span_params = cls(
            end=end,
            name=name,
            start=start,
            trace_id=trace_id,
            xid=xid,
            family=family,
            family_data=family_data,
            message=message,
            metadata=metadata,
            parent_id=parent_id,
            severity=severity,
        )

        return create_span_params
