from modelmetry.guardrails.client import GuardrailsClient
from modelmetry.observability.client import ObservabilityClient


class Configuration:
    def __init__(self, host: str, api_key: str, tenant_id: str):
        self.host = host
        self.api_key = api_key
        self.tenant_id = tenant_id


class Client:
    _configuration: Configuration = None
    _observability: ObservabilityClient = None
    _guardrails: GuardrailsClient = None

    def __init__(
        self, api_key: str, host="https://api.modelmetry.com", tenant_id: str = None
    ):
        self._configuration = Configuration(
            host=host,
            api_key=api_key,
            tenant_id=tenant_id,
        )

    def observability(self) -> ObservabilityClient:
        if not self._observability:
            self._observability = ObservabilityClient(
                tenant_id=self._configuration.tenant_id,
                api_key=self._configuration.api_key,
                host=self._configuration.host,
            )
        return self._observability

    def guardrails(self) -> GuardrailsClient:
        if not self._guardrails:
            self._guardrails = GuardrailsClient(
                api_key=self._configuration.api_key,
                tenant_id=self._configuration.tenant_id,
                host=self._configuration.host,
            )
        return self._guardrails

    def shutdown(self):
        self.observability().shutdown()
