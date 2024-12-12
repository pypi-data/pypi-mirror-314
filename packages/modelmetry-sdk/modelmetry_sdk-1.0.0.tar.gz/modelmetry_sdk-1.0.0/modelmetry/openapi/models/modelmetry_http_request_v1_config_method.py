from typing import Literal, cast

ModelmetryHTTPRequestV1ConfigMethod = Literal["POST"]

MODELMETRY_HTTP_REQUEST_V1_CONFIG_METHOD_VALUES: set[ModelmetryHTTPRequestV1ConfigMethod] = {
    "POST",
}


def check_modelmetry_http_request_v1_config_method(value: str) -> ModelmetryHTTPRequestV1ConfigMethod:
    if value in MODELMETRY_HTTP_REQUEST_V1_CONFIG_METHOD_VALUES:
        return cast(ModelmetryHTTPRequestV1ConfigMethod, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MODELMETRY_HTTP_REQUEST_V1_CONFIG_METHOD_VALUES!r}")
