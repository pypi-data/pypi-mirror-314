from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.modelmetry_embeddings_similarity_v1_config_extraction_method import (
    ModelmetryEmbeddingsSimilarityV1ConfigExtractionMethod,
    check_modelmetry_embeddings_similarity_v1_config_extraction_method,
)
from ..models.modelmetry_embeddings_similarity_v1_config_model import (
    ModelmetryEmbeddingsSimilarityV1ConfigModel,
    check_modelmetry_embeddings_similarity_v1_config_model,
)
from ..models.modelmetry_embeddings_similarity_v1_config_strategy import (
    ModelmetryEmbeddingsSimilarityV1ConfigStrategy,
    check_modelmetry_embeddings_similarity_v1_config_strategy,
)

T = TypeVar("T", bound="ModelmetryEmbeddingsSimilarityV1Config")


@_attrs_define
class ModelmetryEmbeddingsSimilarityV1Config:
    """
    Attributes:
        extraction_method (ModelmetryEmbeddingsSimilarityV1ConfigExtractionMethod): The method to use for extracting
            text strings.
        model (ModelmetryEmbeddingsSimilarityV1ConfigModel): The model to use for encoding text to embeddings (only
            OpenAI models at this stage).
        reference_text (str): The reference text to compare against. Be as detailed or as general as you like.
        strategy (ModelmetryEmbeddingsSimilarityV1ConfigStrategy): The strategy to use for computing similarity.
    """

    extraction_method: ModelmetryEmbeddingsSimilarityV1ConfigExtractionMethod
    model: ModelmetryEmbeddingsSimilarityV1ConfigModel
    reference_text: str
    strategy: ModelmetryEmbeddingsSimilarityV1ConfigStrategy

    def to_dict(self) -> dict[str, Any]:
        extraction_method: str = self.extraction_method

        model: str = self.model

        reference_text = self.reference_text

        strategy: str = self.strategy

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "ExtractionMethod": extraction_method,
                "Model": model,
                "ReferenceText": reference_text,
                "Strategy": strategy,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        extraction_method = check_modelmetry_embeddings_similarity_v1_config_extraction_method(
            d.pop("ExtractionMethod")
        )

        model = check_modelmetry_embeddings_similarity_v1_config_model(d.pop("Model"))

        reference_text = d.pop("ReferenceText")

        strategy = check_modelmetry_embeddings_similarity_v1_config_strategy(d.pop("Strategy"))

        modelmetry_embeddings_similarity_v1_config = cls(
            extraction_method=extraction_method,
            model=model,
            reference_text=reference_text,
            strategy=strategy,
        )

        return modelmetry_embeddings_similarity_v1_config
