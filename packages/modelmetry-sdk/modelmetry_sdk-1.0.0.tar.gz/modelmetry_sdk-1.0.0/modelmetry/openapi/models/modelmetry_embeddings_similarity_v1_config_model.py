from typing import Literal, cast

ModelmetryEmbeddingsSimilarityV1ConfigModel = Literal["openai/text-embedding-3-large", "openai/text-embedding-3-small"]

MODELMETRY_EMBEDDINGS_SIMILARITY_V1_CONFIG_MODEL_VALUES: set[ModelmetryEmbeddingsSimilarityV1ConfigModel] = {
    "openai/text-embedding-3-large",
    "openai/text-embedding-3-small",
}


def check_modelmetry_embeddings_similarity_v1_config_model(value: str) -> ModelmetryEmbeddingsSimilarityV1ConfigModel:
    if value in MODELMETRY_EMBEDDINGS_SIMILARITY_V1_CONFIG_MODEL_VALUES:
        return cast(ModelmetryEmbeddingsSimilarityV1ConfigModel, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODELMETRY_EMBEDDINGS_SIMILARITY_V1_CONFIG_MODEL_VALUES!r}"
    )
