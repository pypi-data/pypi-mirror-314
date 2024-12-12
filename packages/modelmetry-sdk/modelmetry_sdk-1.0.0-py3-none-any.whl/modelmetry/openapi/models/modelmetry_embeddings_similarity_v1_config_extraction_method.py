from typing import Literal, cast

ModelmetryEmbeddingsSimilarityV1ConfigExtractionMethod = Literal[
    "last-user-vs-assistant", "reference-vs-all-messages", "reference-vs-last-assistant", "reference-vs-last-user"
]

MODELMETRY_EMBEDDINGS_SIMILARITY_V1_CONFIG_EXTRACTION_METHOD_VALUES: set[
    ModelmetryEmbeddingsSimilarityV1ConfigExtractionMethod
] = {
    "last-user-vs-assistant",
    "reference-vs-all-messages",
    "reference-vs-last-assistant",
    "reference-vs-last-user",
}


def check_modelmetry_embeddings_similarity_v1_config_extraction_method(
    value: str,
) -> ModelmetryEmbeddingsSimilarityV1ConfigExtractionMethod:
    if value in MODELMETRY_EMBEDDINGS_SIMILARITY_V1_CONFIG_EXTRACTION_METHOD_VALUES:
        return cast(ModelmetryEmbeddingsSimilarityV1ConfigExtractionMethod, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODELMETRY_EMBEDDINGS_SIMILARITY_V1_CONFIG_EXTRACTION_METHOD_VALUES!r}"
    )
