from typing import Literal, cast

ModelmetryEmbeddingsSimilarityV1ConfigStrategy = Literal["cosine", "dot-product", "euclidean-distance"]

MODELMETRY_EMBEDDINGS_SIMILARITY_V1_CONFIG_STRATEGY_VALUES: set[ModelmetryEmbeddingsSimilarityV1ConfigStrategy] = {
    "cosine",
    "dot-product",
    "euclidean-distance",
}


def check_modelmetry_embeddings_similarity_v1_config_strategy(
    value: str,
) -> ModelmetryEmbeddingsSimilarityV1ConfigStrategy:
    if value in MODELMETRY_EMBEDDINGS_SIMILARITY_V1_CONFIG_STRATEGY_VALUES:
        return cast(ModelmetryEmbeddingsSimilarityV1ConfigStrategy, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODELMETRY_EMBEDDINGS_SIMILARITY_V1_CONFIG_STRATEGY_VALUES!r}"
    )
