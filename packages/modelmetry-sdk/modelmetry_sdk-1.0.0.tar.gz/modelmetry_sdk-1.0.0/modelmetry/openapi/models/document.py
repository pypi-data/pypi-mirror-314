from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document_metadata import DocumentMetadata


T = TypeVar("T", bound="Document")


@_attrs_define
class Document:
    """
    Attributes:
        content_type (str):
        identifier (str):
        title (str):
        content (Union[Unset, Any]):
        metadata (Union[Unset, DocumentMetadata]):
    """

    content_type: str
    identifier: str
    title: str
    content: Union[Unset, Any] = UNSET
    metadata: Union[Unset, "DocumentMetadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type

        identifier = self.identifier

        title = self.title

        content = self.content

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "ContentType": content_type,
                "Identifier": identifier,
                "Title": title,
            }
        )
        if content is not UNSET:
            field_dict["Content"] = content
        if metadata is not UNSET:
            field_dict["Metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.document_metadata import DocumentMetadata

        d = src_dict.copy()
        content_type = d.pop("ContentType")

        identifier = d.pop("Identifier")

        title = d.pop("Title")

        content = d.pop("Content", UNSET)

        _metadata = d.pop("Metadata", UNSET)
        metadata: Union[Unset, DocumentMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = DocumentMetadata.from_dict(_metadata)

        document = cls(
            content_type=content_type,
            identifier=identifier,
            title=title,
            content=content,
            metadata=metadata,
        )

        return document
