from typing import Any, Dict, List, Union

from devtools import pprint

from modelmetry.guardrails.response import GuardrailCheckResponse
from modelmetry.openapi import (
    AuthenticatedClient,
    CheckPayloadRequestBody,
    Payload,
    CompletionPayload,
    SystemMessage,
    UserMessage,
    AssistantMessage,
    ToolMessage,
    TextPart,
    check_payload,
)

# create a Message type that's a union of the above four message types
Message = Union[SystemMessage, UserMessage, AssistantMessage, ToolMessage]


class GuardrailsClient:
    client: AuthenticatedClient = None
    tenant_id: str | None = None

    def __init__(
        self,
        api_key: str,
        tenant_id: str | None = None,
        host="https://api.modelmetry.com",
    ):
        if not api_key:
            raise ValueError("api_key is required to instantiate GuardrailsClient")

        self.tenant_id = tenant_id or None
        self.api_key = api_key
        self.client = AuthenticatedClient(
            base_url=host,
            token=api_key,
            auth_header_name="X-API-Key",
            prefix="",
        ).with_headers({"X-API-Key": api_key})

    def check_text(self, text: str, params: Dict[str, Any]) -> GuardrailCheckResponse:
        role = params.get("role", "user")
        if role == "user":
            message = UserMessage(
                role="user",
                contents=[TextPart(text=text)],
            )
        elif role == "system":
            message = SystemMessage(
                role="system",
                contents=[TextPart(text=text)],
            )
        elif role == "assistant":
            message = AssistantMessage(
                role="assistant",
                contents=[TextPart(text=text)],
            )
        elif role == "tool":
            message = ToolMessage(
                role="tool",
                contents=[TextPart(text=text)],
            )
        else:
            raise ValueError(f"Invalid role: {role}")
        return self.check_message(message, params)

    def check_message(
        self, message: Message, params: Dict[str, Any]
    ) -> GuardrailCheckResponse:
        return self.check_messages([message], params)

    def check_messages(
        self, messages: List[Message], params: Dict[str, Any]
    ) -> GuardrailCheckResponse:

        body = CheckPayloadRequestBody(
            tenant_id=self.tenant_id or None,
            guardrail_id=params["guardrail_id"] or "-",
            payload=Payload(
                completion=CompletionPayload(
                    messages=messages,
                )
            ),
        )

        try:
            with self.client as client:
                data = check_payload.sync(client=client, body=body, dryrun=False)
                output = GuardrailCheckResponse(check=data)
                output.check = data
                return output
        except Exception as e:
            pprint(e)
            output = GuardrailCheckResponse(error=e)
            raise e
            return output
