from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.modelmetry_sentiment_analysis_v1_config_model import (
    ModelmetrySentimentAnalysisV1ConfigModel,
    check_modelmetry_sentiment_analysis_v1_config_model,
)
from ..models.modelmetry_sentiment_analysis_v1_config_scope import (
    ModelmetrySentimentAnalysisV1ConfigScope,
    check_modelmetry_sentiment_analysis_v1_config_scope,
)

T = TypeVar("T", bound="ModelmetrySentimentAnalysisV1Config")


@_attrs_define
class ModelmetrySentimentAnalysisV1Config:
    """
    Attributes:
        model (ModelmetrySentimentAnalysisV1ConfigModel): The model to use. Default: 'openai/gpt-4o-mini'.
        scope (ModelmetrySentimentAnalysisV1ConfigScope):
    """

    scope: ModelmetrySentimentAnalysisV1ConfigScope
    model: ModelmetrySentimentAnalysisV1ConfigModel = "openai/gpt-4o-mini"

    def to_dict(self) -> dict[str, Any]:
        model: str = self.model

        scope: str = self.scope

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Model": model,
                "Scope": scope,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        model = check_modelmetry_sentiment_analysis_v1_config_model(d.pop("Model"))

        scope = check_modelmetry_sentiment_analysis_v1_config_scope(d.pop("Scope"))

        modelmetry_sentiment_analysis_v1_config = cls(
            model=model,
            scope=scope,
        )

        return modelmetry_sentiment_analysis_v1_config
