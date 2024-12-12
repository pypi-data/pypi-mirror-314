from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.modelmetry_http_request_v1_config_method import (
    ModelmetryHTTPRequestV1ConfigMethod,
    check_modelmetry_http_request_v1_config_method,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.modelmetry_http_request_v1_config_headers import ModelmetryHTTPRequestV1ConfigHeaders


T = TypeVar("T", bound="ModelmetryHTTPRequestV1Config")


@_attrs_define
class ModelmetryHTTPRequestV1Config:
    """
    Attributes:
        headers (ModelmetryHTTPRequestV1ConfigHeaders): A map of headers to include in the request.
        method (ModelmetryHTTPRequestV1ConfigMethod): The HTTP method to use for the request. Default: 'POST'.
        url (str): The URL to send the HTTP request to.
        findings_json_path (Union[None, Unset, str]): The JSON path to the findings in the response body.
        message_json_path (Union[None, Unset, str]): The JSON path to the message in the response body.
        outcome_json_path (Union[None, Unset, str]): The JSON path to the outcome in the response body.
    """

    headers: "ModelmetryHTTPRequestV1ConfigHeaders"
    url: str
    method: ModelmetryHTTPRequestV1ConfigMethod = "POST"
    findings_json_path: Union[None, Unset, str] = UNSET
    message_json_path: Union[None, Unset, str] = UNSET
    outcome_json_path: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        headers = self.headers.to_dict()

        method: str = self.method

        url = self.url

        findings_json_path: Union[None, Unset, str]
        if isinstance(self.findings_json_path, Unset):
            findings_json_path = UNSET
        else:
            findings_json_path = self.findings_json_path

        message_json_path: Union[None, Unset, str]
        if isinstance(self.message_json_path, Unset):
            message_json_path = UNSET
        else:
            message_json_path = self.message_json_path

        outcome_json_path: Union[None, Unset, str]
        if isinstance(self.outcome_json_path, Unset):
            outcome_json_path = UNSET
        else:
            outcome_json_path = self.outcome_json_path

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "Headers": headers,
                "Method": method,
                "URL": url,
            }
        )
        if findings_json_path is not UNSET:
            field_dict["FindingsJSONPath"] = findings_json_path
        if message_json_path is not UNSET:
            field_dict["MessageJSONPath"] = message_json_path
        if outcome_json_path is not UNSET:
            field_dict["OutcomeJSONPath"] = outcome_json_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.modelmetry_http_request_v1_config_headers import ModelmetryHTTPRequestV1ConfigHeaders

        d = src_dict.copy()
        headers = ModelmetryHTTPRequestV1ConfigHeaders.from_dict(d.pop("Headers"))

        method = check_modelmetry_http_request_v1_config_method(d.pop("Method"))

        url = d.pop("URL")

        def _parse_findings_json_path(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        findings_json_path = _parse_findings_json_path(d.pop("FindingsJSONPath", UNSET))

        def _parse_message_json_path(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        message_json_path = _parse_message_json_path(d.pop("MessageJSONPath", UNSET))

        def _parse_outcome_json_path(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        outcome_json_path = _parse_outcome_json_path(d.pop("OutcomeJSONPath", UNSET))

        modelmetry_http_request_v1_config = cls(
            headers=headers,
            method=method,
            url=url,
            findings_json_path=findings_json_path,
            message_json_path=message_json_path,
            outcome_json_path=outcome_json_path,
        )

        return modelmetry_http_request_v1_config
