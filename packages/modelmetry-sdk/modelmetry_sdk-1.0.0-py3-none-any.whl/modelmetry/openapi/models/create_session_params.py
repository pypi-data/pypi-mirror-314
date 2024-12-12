from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_session_params_metadata import CreateSessionParamsMetadata


T = TypeVar("T", bound="CreateSessionParams")


@_attrs_define
class CreateSessionParams:
    """
    Attributes:
        xid (str):
        metadata (Union[Unset, CreateSessionParamsMetadata]):
        name (Union[None, Unset, str]):
    """

    xid: str
    metadata: Union[Unset, "CreateSessionParamsMetadata"] = UNSET
    name: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        xid = self.xid

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "XID": xid,
            }
        )
        if metadata is not UNSET:
            field_dict["Metadata"] = metadata
        if name is not UNSET:
            field_dict["Name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_session_params_metadata import CreateSessionParamsMetadata

        d = src_dict.copy()
        xid = d.pop("XID")

        _metadata = d.pop("Metadata", UNSET)
        metadata: Union[Unset, CreateSessionParamsMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreateSessionParamsMetadata.from_dict(_metadata)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("Name", UNSET))

        create_session_params = cls(
            xid=xid,
            metadata=metadata,
            name=name,
        )

        return create_session_params
