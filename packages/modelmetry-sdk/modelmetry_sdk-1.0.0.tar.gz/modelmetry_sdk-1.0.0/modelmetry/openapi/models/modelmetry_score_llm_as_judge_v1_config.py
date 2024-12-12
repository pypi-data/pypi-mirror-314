from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.modelmetry_score_llm_as_judge_v1_config_model import (
    ModelmetryScoreLLMAsJudgeV1ConfigModel,
    check_modelmetry_score_llm_as_judge_v1_config_model,
)

T = TypeVar("T", bound="ModelmetryScoreLLMAsJudgeV1Config")


@_attrs_define
class ModelmetryScoreLLMAsJudgeV1Config:
    """
    Attributes:
        finding_name (str): The name of the finding to use for the result (e.g., threatening_level, about_hotel_score).
        instructions (str): You are an LLM evaluator. Please score from 0.0 to 1.0 how likely the user is to be
            satisfied with this answer, from 0.0 being not satisfied at all to 1.0 being completely satisfied.
        max_tokens (int): The limit on the number of tokens the entire prompt can be. Default: 8192.
        model (ModelmetryScoreLLMAsJudgeV1ConfigModel): The model to use. Default: 'openai/gpt-4o-mini'.
    """

    finding_name: str
    instructions: str
    max_tokens: int = 8192
    model: ModelmetryScoreLLMAsJudgeV1ConfigModel = "openai/gpt-4o-mini"

    def to_dict(self) -> dict[str, Any]:
        finding_name = self.finding_name

        instructions = self.instructions

        max_tokens = self.max_tokens

        model: str = self.model

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "FindingName": finding_name,
                "Instructions": instructions,
                "MaxTokens": max_tokens,
                "Model": model,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        finding_name = d.pop("FindingName")

        instructions = d.pop("Instructions")

        max_tokens = d.pop("MaxTokens")

        model = check_modelmetry_score_llm_as_judge_v1_config_model(d.pop("Model"))

        modelmetry_score_llm_as_judge_v1_config = cls(
            finding_name=finding_name,
            instructions=instructions,
            max_tokens=max_tokens,
            model=model,
        )

        return modelmetry_score_llm_as_judge_v1_config
