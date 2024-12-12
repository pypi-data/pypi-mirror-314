from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.document import Document
    from ..models.retrieval_query import RetrievalQuery


T = TypeVar("T", bound="RetrievalFamilyData")


@_attrs_define
class RetrievalFamilyData:
    """
    Attributes:
        documents (Union[None, list['Document']]):
        queries (Union[None, list['RetrievalQuery']]):
    """

    documents: Union[None, list["Document"]]
    queries: Union[None, list["RetrievalQuery"]]

    def to_dict(self) -> dict[str, Any]:
        documents: Union[None, list[dict[str, Any]]]
        if isinstance(self.documents, list):
            documents = []
            for documents_type_0_item_data in self.documents:
                documents_type_0_item = documents_type_0_item_data.to_dict()
                documents.append(documents_type_0_item)

        else:
            documents = self.documents

        queries: Union[None, list[dict[str, Any]]]
        if isinstance(self.queries, list):
            queries = []
            for queries_type_0_item_data in self.queries:
                queries_type_0_item = queries_type_0_item_data.to_dict()
                queries.append(queries_type_0_item)

        else:
            queries = self.queries

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Documents": documents,
                "Queries": queries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.document import Document
        from ..models.retrieval_query import RetrievalQuery

        d = src_dict.copy()

        def _parse_documents(data: object) -> Union[None, list["Document"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                documents_type_0 = []
                _documents_type_0 = data
                for documents_type_0_item_data in _documents_type_0:
                    documents_type_0_item = Document.from_dict(documents_type_0_item_data)

                    documents_type_0.append(documents_type_0_item)

                return documents_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["Document"]], data)

        documents = _parse_documents(d.pop("Documents"))

        def _parse_queries(data: object) -> Union[None, list["RetrievalQuery"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                queries_type_0 = []
                _queries_type_0 = data
                for queries_type_0_item_data in _queries_type_0:
                    queries_type_0_item = RetrievalQuery.from_dict(queries_type_0_item_data)

                    queries_type_0.append(queries_type_0_item)

                return queries_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["RetrievalQuery"]], data)

        queries = _parse_queries(d.pop("Queries"))

        retrieval_family_data = cls(
            documents=documents,
            queries=queries,
        )

        return retrieval_family_data
