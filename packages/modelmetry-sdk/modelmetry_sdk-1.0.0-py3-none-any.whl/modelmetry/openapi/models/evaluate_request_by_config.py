from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.evaluate_request_by_config_config import EvaluateRequestByConfigConfig
    from ..models.grading_configuration import GradingConfiguration
    from ..models.payload import Payload


T = TypeVar("T", bound="EvaluateRequestByConfig")


@_attrs_define
class EvaluateRequestByConfig:
    """
    Attributes:
        config (EvaluateRequestByConfigConfig):
        evaluator_id (str):
        payload (Payload):
        grading (Union[Unset, GradingConfiguration]):
        secrets (Union[None, Unset, list[str]]):
    """

    config: "EvaluateRequestByConfigConfig"
    evaluator_id: str
    payload: "Payload"
    grading: Union[Unset, "GradingConfiguration"] = UNSET
    secrets: Union[None, Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        config = self.config.to_dict()

        evaluator_id = self.evaluator_id

        payload = self.payload.to_dict()

        grading: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.grading, Unset):
            grading = self.grading.to_dict()

        secrets: Union[None, Unset, list[str]]
        if isinstance(self.secrets, Unset):
            secrets = UNSET
        elif isinstance(self.secrets, list):
            secrets = self.secrets

        else:
            secrets = self.secrets

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Config": config,
                "EvaluatorID": evaluator_id,
                "Payload": payload,
            }
        )
        if grading is not UNSET:
            field_dict["Grading"] = grading
        if secrets is not UNSET:
            field_dict["Secrets"] = secrets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.evaluate_request_by_config_config import EvaluateRequestByConfigConfig
        from ..models.grading_configuration import GradingConfiguration
        from ..models.payload import Payload

        d = src_dict.copy()
        config = EvaluateRequestByConfigConfig.from_dict(d.pop("Config"))

        evaluator_id = d.pop("EvaluatorID")

        payload = Payload.from_dict(d.pop("Payload"))

        _grading = d.pop("Grading", UNSET)
        grading: Union[Unset, GradingConfiguration]
        if isinstance(_grading, Unset):
            grading = UNSET
        else:
            grading = GradingConfiguration.from_dict(_grading)

        def _parse_secrets(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                secrets_type_0 = cast(list[str], data)

                return secrets_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        secrets = _parse_secrets(d.pop("Secrets", UNSET))

        evaluate_request_by_config = cls(
            config=config,
            evaluator_id=evaluator_id,
            payload=payload,
            grading=grading,
            secrets=secrets,
        )

        return evaluate_request_by_config
