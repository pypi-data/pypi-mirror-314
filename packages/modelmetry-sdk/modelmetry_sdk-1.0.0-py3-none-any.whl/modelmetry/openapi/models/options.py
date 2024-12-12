from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.options_logit_bias import OptionsLogitBias
    from ..models.options_response_format import OptionsResponseFormat
    from ..models.options_stop import OptionsStop
    from ..models.tool import Tool


T = TypeVar("T", bound="Options")


@_attrs_define
class Options:
    """
    Attributes:
        api_key (Union[Unset, str]):
        api_version (Union[Unset, str]):
        base_url (Union[Unset, str]):
        deployment_id (Union[Unset, str]):
        frequency_penalty (Union[Unset, float]):
        function_call (Union[Unset, str]):
        functions (Union[None, Unset, list[str]]):
        logit_bias (Union[Unset, OptionsLogitBias]):
        logprobs (Union[Unset, bool]):
        max_tokens (Union[Unset, int]):
        model (Union[Unset, str]):
        model_list (Union[None, Unset, list[str]]):
        n (Union[Unset, int]):
        presence_penalty (Union[Unset, float]):
        provider (Union[Unset, str]):
        response_format (Union[Unset, OptionsResponseFormat]):
        seed (Union[Unset, int]):
        stop (Union[Unset, OptionsStop]):
        stream (Union[Unset, bool]):
        temperature (Union[Unset, float]):
        timeout (Union[Unset, float]):
        tool_choice (Union[Unset, str]):
        tools (Union[None, Unset, list['Tool']]):
        top_logprobs (Union[Unset, int]):
        top_p (Union[Unset, float]):
        user (Union[Unset, str]):
    """

    api_key: Union[Unset, str] = UNSET
    api_version: Union[Unset, str] = UNSET
    base_url: Union[Unset, str] = UNSET
    deployment_id: Union[Unset, str] = UNSET
    frequency_penalty: Union[Unset, float] = UNSET
    function_call: Union[Unset, str] = UNSET
    functions: Union[None, Unset, list[str]] = UNSET
    logit_bias: Union[Unset, "OptionsLogitBias"] = UNSET
    logprobs: Union[Unset, bool] = UNSET
    max_tokens: Union[Unset, int] = UNSET
    model: Union[Unset, str] = UNSET
    model_list: Union[None, Unset, list[str]] = UNSET
    n: Union[Unset, int] = UNSET
    presence_penalty: Union[Unset, float] = UNSET
    provider: Union[Unset, str] = UNSET
    response_format: Union[Unset, "OptionsResponseFormat"] = UNSET
    seed: Union[Unset, int] = UNSET
    stop: Union[Unset, "OptionsStop"] = UNSET
    stream: Union[Unset, bool] = UNSET
    temperature: Union[Unset, float] = UNSET
    timeout: Union[Unset, float] = UNSET
    tool_choice: Union[Unset, str] = UNSET
    tools: Union[None, Unset, list["Tool"]] = UNSET
    top_logprobs: Union[Unset, int] = UNSET
    top_p: Union[Unset, float] = UNSET
    user: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        api_key = self.api_key

        api_version = self.api_version

        base_url = self.base_url

        deployment_id = self.deployment_id

        frequency_penalty = self.frequency_penalty

        function_call = self.function_call

        functions: Union[None, Unset, list[str]]
        if isinstance(self.functions, Unset):
            functions = UNSET
        elif isinstance(self.functions, list):
            functions = self.functions

        else:
            functions = self.functions

        logit_bias: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.logit_bias, Unset):
            logit_bias = self.logit_bias.to_dict()

        logprobs = self.logprobs

        max_tokens = self.max_tokens

        model = self.model

        model_list: Union[None, Unset, list[str]]
        if isinstance(self.model_list, Unset):
            model_list = UNSET
        elif isinstance(self.model_list, list):
            model_list = self.model_list

        else:
            model_list = self.model_list

        n = self.n

        presence_penalty = self.presence_penalty

        provider = self.provider

        response_format: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.response_format, Unset):
            response_format = self.response_format.to_dict()

        seed = self.seed

        stop: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.stop, Unset):
            stop = self.stop.to_dict()

        stream = self.stream

        temperature = self.temperature

        timeout = self.timeout

        tool_choice = self.tool_choice

        tools: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.tools, Unset):
            tools = UNSET
        elif isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item = tools_type_0_item_data.to_dict()
                tools.append(tools_type_0_item)

        else:
            tools = self.tools

        top_logprobs = self.top_logprobs

        top_p = self.top_p

        user = self.user

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if api_key is not UNSET:
            field_dict["APIKey"] = api_key
        if api_version is not UNSET:
            field_dict["APIVersion"] = api_version
        if base_url is not UNSET:
            field_dict["BaseURL"] = base_url
        if deployment_id is not UNSET:
            field_dict["DeploymentID"] = deployment_id
        if frequency_penalty is not UNSET:
            field_dict["FrequencyPenalty"] = frequency_penalty
        if function_call is not UNSET:
            field_dict["FunctionCall"] = function_call
        if functions is not UNSET:
            field_dict["Functions"] = functions
        if logit_bias is not UNSET:
            field_dict["LogitBias"] = logit_bias
        if logprobs is not UNSET:
            field_dict["Logprobs"] = logprobs
        if max_tokens is not UNSET:
            field_dict["MaxTokens"] = max_tokens
        if model is not UNSET:
            field_dict["Model"] = model
        if model_list is not UNSET:
            field_dict["ModelList"] = model_list
        if n is not UNSET:
            field_dict["N"] = n
        if presence_penalty is not UNSET:
            field_dict["PresencePenalty"] = presence_penalty
        if provider is not UNSET:
            field_dict["Provider"] = provider
        if response_format is not UNSET:
            field_dict["ResponseFormat"] = response_format
        if seed is not UNSET:
            field_dict["Seed"] = seed
        if stop is not UNSET:
            field_dict["Stop"] = stop
        if stream is not UNSET:
            field_dict["Stream"] = stream
        if temperature is not UNSET:
            field_dict["Temperature"] = temperature
        if timeout is not UNSET:
            field_dict["Timeout"] = timeout
        if tool_choice is not UNSET:
            field_dict["ToolChoice"] = tool_choice
        if tools is not UNSET:
            field_dict["Tools"] = tools
        if top_logprobs is not UNSET:
            field_dict["TopLogprobs"] = top_logprobs
        if top_p is not UNSET:
            field_dict["TopP"] = top_p
        if user is not UNSET:
            field_dict["User"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.options_logit_bias import OptionsLogitBias
        from ..models.options_response_format import OptionsResponseFormat
        from ..models.options_stop import OptionsStop
        from ..models.tool import Tool

        d = src_dict.copy()
        api_key = d.pop("APIKey", UNSET)

        api_version = d.pop("APIVersion", UNSET)

        base_url = d.pop("BaseURL", UNSET)

        deployment_id = d.pop("DeploymentID", UNSET)

        frequency_penalty = d.pop("FrequencyPenalty", UNSET)

        function_call = d.pop("FunctionCall", UNSET)

        def _parse_functions(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                functions_type_0 = cast(list[str], data)

                return functions_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        functions = _parse_functions(d.pop("Functions", UNSET))

        _logit_bias = d.pop("LogitBias", UNSET)
        logit_bias: Union[Unset, OptionsLogitBias]
        if isinstance(_logit_bias, Unset):
            logit_bias = UNSET
        else:
            logit_bias = OptionsLogitBias.from_dict(_logit_bias)

        logprobs = d.pop("Logprobs", UNSET)

        max_tokens = d.pop("MaxTokens", UNSET)

        model = d.pop("Model", UNSET)

        def _parse_model_list(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                model_list_type_0 = cast(list[str], data)

                return model_list_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        model_list = _parse_model_list(d.pop("ModelList", UNSET))

        n = d.pop("N", UNSET)

        presence_penalty = d.pop("PresencePenalty", UNSET)

        provider = d.pop("Provider", UNSET)

        _response_format = d.pop("ResponseFormat", UNSET)
        response_format: Union[Unset, OptionsResponseFormat]
        if isinstance(_response_format, Unset):
            response_format = UNSET
        else:
            response_format = OptionsResponseFormat.from_dict(_response_format)

        seed = d.pop("Seed", UNSET)

        _stop = d.pop("Stop", UNSET)
        stop: Union[Unset, OptionsStop]
        if isinstance(_stop, Unset):
            stop = UNSET
        else:
            stop = OptionsStop.from_dict(_stop)

        stream = d.pop("Stream", UNSET)

        temperature = d.pop("Temperature", UNSET)

        timeout = d.pop("Timeout", UNSET)

        tool_choice = d.pop("ToolChoice", UNSET)

        def _parse_tools(data: object) -> Union[None, Unset, list["Tool"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tools_type_0 = []
                _tools_type_0 = data
                for tools_type_0_item_data in _tools_type_0:
                    tools_type_0_item = Tool.from_dict(tools_type_0_item_data)

                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["Tool"]], data)

        tools = _parse_tools(d.pop("Tools", UNSET))

        top_logprobs = d.pop("TopLogprobs", UNSET)

        top_p = d.pop("TopP", UNSET)

        user = d.pop("User", UNSET)

        options = cls(
            api_key=api_key,
            api_version=api_version,
            base_url=base_url,
            deployment_id=deployment_id,
            frequency_penalty=frequency_penalty,
            function_call=function_call,
            functions=functions,
            logit_bias=logit_bias,
            logprobs=logprobs,
            max_tokens=max_tokens,
            model=model,
            model_list=model_list,
            n=n,
            presence_penalty=presence_penalty,
            provider=provider,
            response_format=response_format,
            seed=seed,
            stop=stop,
            stream=stream,
            temperature=temperature,
            timeout=timeout,
            tool_choice=tool_choice,
            tools=tools,
            top_logprobs=top_logprobs,
            top_p=top_p,
            user=user,
        )

        return options
