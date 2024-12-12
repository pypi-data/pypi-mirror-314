from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.modelmetry_boolean_llm_as_judge_v1_config_model import (
    ModelmetryBooleanLLMAsJudgeV1ConfigModel,
    check_modelmetry_boolean_llm_as_judge_v1_config_model,
)

T = TypeVar("T", bound="ModelmetryBooleanLLMAsJudgeV1Config")


@_attrs_define
class ModelmetryBooleanLLMAsJudgeV1Config:
    """
    Attributes:
        finding_name (str): The name of the finding to use for this evaluator's boolean output (e.g., is_threatening,
            is_about_hotels).
        instructions (str): You are an LLM evaluator. We need the guarantee that the output answers what is being asked
            on the input, please evaluate as False if it doesn't.
        max_tokens (int): The limit on the number of tokens the entire prompt can be. Default: 8192.
        model (ModelmetryBooleanLLMAsJudgeV1ConfigModel): The model to use. Default: 'openai/gpt-4o-mini'.
    """

    finding_name: str
    instructions: str
    max_tokens: int = 8192
    model: ModelmetryBooleanLLMAsJudgeV1ConfigModel = "openai/gpt-4o-mini"

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

        model = check_modelmetry_boolean_llm_as_judge_v1_config_model(d.pop("Model"))

        modelmetry_boolean_llm_as_judge_v1_config = cls(
            finding_name=finding_name,
            instructions=instructions,
            max_tokens=max_tokens,
            model=model,
        )

        return modelmetry_boolean_llm_as_judge_v1_config
