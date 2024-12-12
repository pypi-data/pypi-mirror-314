from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RetrievalQuery")


@_attrs_define
class RetrievalQuery:
    """
    Attributes:
        text_representation (str):
        embeddings (Union[None, Unset, list[float]]):
    """

    text_representation: str
    embeddings: Union[None, Unset, list[float]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        text_representation = self.text_representation

        embeddings: Union[None, Unset, list[float]]
        if isinstance(self.embeddings, Unset):
            embeddings = UNSET
        elif isinstance(self.embeddings, list):
            embeddings = self.embeddings

        else:
            embeddings = self.embeddings

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "TextRepresentation": text_representation,
            }
        )
        if embeddings is not UNSET:
            field_dict["Embeddings"] = embeddings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        text_representation = d.pop("TextRepresentation")

        def _parse_embeddings(data: object) -> Union[None, Unset, list[float]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                embeddings_type_0 = cast(list[float], data)

                return embeddings_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[float]], data)

        embeddings = _parse_embeddings(d.pop("Embeddings", UNSET))

        retrieval_query = cls(
            text_representation=text_representation,
            embeddings=embeddings,
        )

        return retrieval_query
