from typing import Literal, cast

ModelmetryBooleanLLMAsJudgeV1ConfigModel = Literal[
    "google/gemini-1.5-flash",
    "google/gemini-1.5-pro",
    "groq/gemma-7b-it",
    "groq/llama3-70b-8192",
    "groq/llama3-8b-8192",
    "groq/mixtral-8x7b-32768",
    "openai/gpt-3.5-turbo",
    "openai/gpt-4o",
    "openai/gpt-4o-mini",
]

MODELMETRY_BOOLEAN_LLM_AS_JUDGE_V1_CONFIG_MODEL_VALUES: set[ModelmetryBooleanLLMAsJudgeV1ConfigModel] = {
    "google/gemini-1.5-flash",
    "google/gemini-1.5-pro",
    "groq/gemma-7b-it",
    "groq/llama3-70b-8192",
    "groq/llama3-8b-8192",
    "groq/mixtral-8x7b-32768",
    "openai/gpt-3.5-turbo",
    "openai/gpt-4o",
    "openai/gpt-4o-mini",
}


def check_modelmetry_boolean_llm_as_judge_v1_config_model(value: str) -> ModelmetryBooleanLLMAsJudgeV1ConfigModel:
    if value in MODELMETRY_BOOLEAN_LLM_AS_JUDGE_V1_CONFIG_MODEL_VALUES:
        return cast(ModelmetryBooleanLLMAsJudgeV1ConfigModel, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODELMETRY_BOOLEAN_LLM_AS_JUDGE_V1_CONFIG_MODEL_VALUES!r}"
    )
