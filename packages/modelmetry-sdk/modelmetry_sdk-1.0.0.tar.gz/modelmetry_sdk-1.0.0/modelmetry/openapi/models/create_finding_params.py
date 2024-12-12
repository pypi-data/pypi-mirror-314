import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.create_finding_params_source import CreateFindingParamsSource, check_create_finding_params_source
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_finding_params_metadata import CreateFindingParamsMetadata


T = TypeVar("T", bound="CreateFindingParams")


@_attrs_define
class CreateFindingParams:
    """
    Attributes:
        name (str):
        value (Union[bool, float, str]):
        xid (str):
        at (Union[None, Unset, datetime.datetime]):
        comment (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        entry_id (Union[None, Unset, str]):
        metadata (Union[Unset, CreateFindingParamsMetadata]):
        source (Union[Unset, CreateFindingParamsSource]):  Default: 'annotation'.
        span_id (Union[None, Unset, str]):
        trace_id (Union[None, Unset, str]):
    """

    name: str
    value: Union[bool, float, str]
    xid: str
    at: Union[None, Unset, datetime.datetime] = UNSET
    comment: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    entry_id: Union[None, Unset, str] = UNSET
    metadata: Union[Unset, "CreateFindingParamsMetadata"] = UNSET
    source: Union[Unset, CreateFindingParamsSource] = "annotation"
    span_id: Union[None, Unset, str] = UNSET
    trace_id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value: Union[bool, float, str]
        value = self.value

        xid = self.xid

        at: Union[None, Unset, str]
        if isinstance(self.at, Unset):
            at = UNSET
        elif isinstance(self.at, datetime.datetime):
            at = self.at.isoformat()
        else:
            at = self.at

        comment: Union[None, Unset, str]
        if isinstance(self.comment, Unset):
            comment = UNSET
        else:
            comment = self.comment

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        entry_id: Union[None, Unset, str]
        if isinstance(self.entry_id, Unset):
            entry_id = UNSET
        else:
            entry_id = self.entry_id

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source

        span_id: Union[None, Unset, str]
        if isinstance(self.span_id, Unset):
            span_id = UNSET
        else:
            span_id = self.span_id

        trace_id: Union[None, Unset, str]
        if isinstance(self.trace_id, Unset):
            trace_id = UNSET
        else:
            trace_id = self.trace_id

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Name": name,
                "Value": value,
                "XID": xid,
            }
        )
        if at is not UNSET:
            field_dict["At"] = at
        if comment is not UNSET:
            field_dict["Comment"] = comment
        if description is not UNSET:
            field_dict["Description"] = description
        if entry_id is not UNSET:
            field_dict["EntryID"] = entry_id
        if metadata is not UNSET:
            field_dict["Metadata"] = metadata
        if source is not UNSET:
            field_dict["Source"] = source
        if span_id is not UNSET:
            field_dict["SpanID"] = span_id
        if trace_id is not UNSET:
            field_dict["TraceID"] = trace_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_finding_params_metadata import CreateFindingParamsMetadata

        d = src_dict.copy()
        name = d.pop("Name")

        def _parse_value(data: object) -> Union[bool, float, str]:
            return cast(Union[bool, float, str], data)

        value = _parse_value(d.pop("Value"))

        xid = d.pop("XID")

        def _parse_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                at_type_0 = isoparse(data)

                return at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        at = _parse_at(d.pop("At", UNSET))

        def _parse_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment = _parse_comment(d.pop("Comment", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("Description", UNSET))

        def _parse_entry_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        entry_id = _parse_entry_id(d.pop("EntryID", UNSET))

        _metadata = d.pop("Metadata", UNSET)
        metadata: Union[Unset, CreateFindingParamsMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreateFindingParamsMetadata.from_dict(_metadata)

        _source = d.pop("Source", UNSET)
        source: Union[Unset, CreateFindingParamsSource]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = check_create_finding_params_source(_source)

        def _parse_span_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        span_id = _parse_span_id(d.pop("SpanID", UNSET))

        def _parse_trace_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        trace_id = _parse_trace_id(d.pop("TraceID", UNSET))

        create_finding_params = cls(
            name=name,
            value=value,
            xid=xid,
            at=at,
            comment=comment,
            description=description,
            entry_id=entry_id,
            metadata=metadata,
            source=source,
            span_id=span_id,
            trace_id=trace_id,
        )

        return create_finding_params
