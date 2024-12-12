from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="AzurePromptShieldsV1Config")


@_attrs_define
class AzurePromptShieldsV1Config:
    """
    Attributes:
        endpoint (str): The endpoint of the Azure Prompt Shields API.
    """

    endpoint: str

    def to_dict(self) -> dict[str, Any]:
        endpoint = self.endpoint

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Endpoint": endpoint,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        endpoint = d.pop("Endpoint")

        azure_prompt_shields_v1_config = cls(
            endpoint=endpoint,
        )

        return azure_prompt_shields_v1_config
