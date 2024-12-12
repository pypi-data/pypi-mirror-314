from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.evaluate_request_by_config import EvaluateRequestByConfig
    from ..models.evaluate_request_by_entry import EvaluateRequestByEntry
    from ..models.evaluate_request_by_instance import EvaluateRequestByInstance


T = TypeVar("T", bound="EvaluateRequestBody")


@_attrs_define
class EvaluateRequestBody:
    """
    Attributes:
        tenant_id (str):
        schema (Union[Unset, str]): A URL to the JSON Schema for this object.
        by_config (Union[Unset, EvaluateRequestByConfig]):
        by_entry (Union[Unset, EvaluateRequestByEntry]):
        by_instance (Union[Unset, EvaluateRequestByInstance]):
        persist (Union[None, Unset, bool]):
    """

    tenant_id: str
    schema: Union[Unset, str] = UNSET
    by_config: Union[Unset, "EvaluateRequestByConfig"] = UNSET
    by_entry: Union[Unset, "EvaluateRequestByEntry"] = UNSET
    by_instance: Union[Unset, "EvaluateRequestByInstance"] = UNSET
    persist: Union[None, Unset, bool] = UNSET

    def to_dict(self) -> dict[str, Any]:
        tenant_id = self.tenant_id

        schema = self.schema

        by_config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.by_config, Unset):
            by_config = self.by_config.to_dict()

        by_entry: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.by_entry, Unset):
            by_entry = self.by_entry.to_dict()

        by_instance: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.by_instance, Unset):
            by_instance = self.by_instance.to_dict()

        persist: Union[None, Unset, bool]
        if isinstance(self.persist, Unset):
            persist = UNSET
        else:
            persist = self.persist

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "TenantID": tenant_id,
            }
        )
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if by_config is not UNSET:
            field_dict["ByConfig"] = by_config
        if by_entry is not UNSET:
            field_dict["ByEntry"] = by_entry
        if by_instance is not UNSET:
            field_dict["ByInstance"] = by_instance
        if persist is not UNSET:
            field_dict["Persist"] = persist

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.evaluate_request_by_config import EvaluateRequestByConfig
        from ..models.evaluate_request_by_entry import EvaluateRequestByEntry
        from ..models.evaluate_request_by_instance import EvaluateRequestByInstance

        d = src_dict.copy()
        tenant_id = d.pop("TenantID")

        schema = d.pop("$schema", UNSET)

        _by_config = d.pop("ByConfig", UNSET)
        by_config: Union[Unset, EvaluateRequestByConfig]
        if isinstance(_by_config, Unset):
            by_config = UNSET
        else:
            by_config = EvaluateRequestByConfig.from_dict(_by_config)

        _by_entry = d.pop("ByEntry", UNSET)
        by_entry: Union[Unset, EvaluateRequestByEntry]
        if isinstance(_by_entry, Unset):
            by_entry = UNSET
        else:
            by_entry = EvaluateRequestByEntry.from_dict(_by_entry)

        _by_instance = d.pop("ByInstance", UNSET)
        by_instance: Union[Unset, EvaluateRequestByInstance]
        if isinstance(_by_instance, Unset):
            by_instance = UNSET
        else:
            by_instance = EvaluateRequestByInstance.from_dict(_by_instance)

        def _parse_persist(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        persist = _parse_persist(d.pop("Persist", UNSET))

        evaluate_request_body = cls(
            tenant_id=tenant_id,
            schema=schema,
            by_config=by_config,
            by_entry=by_entry,
            by_instance=by_instance,
            persist=persist,
        )

        return evaluate_request_body
