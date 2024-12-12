import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.simplified_finding_source import SimplifiedFindingSource, check_simplified_finding_source

if TYPE_CHECKING:
    from ..models.simplified_finding_metadata import SimplifiedFindingMetadata


T = TypeVar("T", bound="SimplifiedFinding")


@_attrs_define
class SimplifiedFinding:
    """
    Attributes:
        comment (str):
        created_at (datetime.datetime):
        evaluator_id (Union[None, str]):
        metadata (SimplifiedFindingMetadata):
        name (str):
        source (SimplifiedFindingSource):  Default: 'annotation'.
        value (Union[bool, float, str]):
    """

    comment: str
    created_at: datetime.datetime
    evaluator_id: Union[None, str]
    metadata: "SimplifiedFindingMetadata"
    name: str
    value: Union[bool, float, str]
    source: SimplifiedFindingSource = "annotation"

    def to_dict(self) -> dict[str, Any]:
        comment = self.comment

        created_at = self.created_at.isoformat()

        evaluator_id: Union[None, str]
        evaluator_id = self.evaluator_id

        metadata = self.metadata.to_dict()

        name = self.name

        source: str = self.source

        value: Union[bool, float, str]
        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Comment": comment,
                "CreatedAt": created_at,
                "EvaluatorID": evaluator_id,
                "Metadata": metadata,
                "Name": name,
                "Source": source,
                "Value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.simplified_finding_metadata import SimplifiedFindingMetadata

        d = src_dict.copy()
        comment = d.pop("Comment")

        created_at = isoparse(d.pop("CreatedAt"))

        def _parse_evaluator_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        evaluator_id = _parse_evaluator_id(d.pop("EvaluatorID"))

        metadata = SimplifiedFindingMetadata.from_dict(d.pop("Metadata"))

        name = d.pop("Name")

        source = check_simplified_finding_source(d.pop("Source"))

        def _parse_value(data: object) -> Union[bool, float, str]:
            return cast(Union[bool, float, str], data)

        value = _parse_value(d.pop("Value"))

        simplified_finding = cls(
            comment=comment,
            created_at=created_at,
            evaluator_id=evaluator_id,
            metadata=metadata,
            name=name,
            source=source,
            value=value,
        )

        return simplified_finding
