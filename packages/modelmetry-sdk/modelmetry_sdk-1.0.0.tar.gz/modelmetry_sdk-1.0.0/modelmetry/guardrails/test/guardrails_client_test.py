from datetime import date
import unittest
from unittest.mock import MagicMock

from modelmetry.guardrails.response import GuardrailCheckResponse
from modelmetry.guardrails.client import GuardrailsClient
from modelmetry.openapi.client import AuthenticatedClient


class TestGuardrailsClient(unittest.TestCase):
    def test_instanciate_without_api_key_should_fail(self):
        with self.assertRaises(ValueError):
            GuardrailsClient("")

    def test_instanciate_normal(self):
        client = GuardrailsClient("api_key")
        self.assertIsNotNone(client)
        self.assertIsInstance(client, GuardrailsClient)
        self.assertIsInstance(client.client, AuthenticatedClient)
        self.assertEqual(client.api_key, "api_key")
        self.assertIsNone(client.tenant_id)

    def test_check_transport_error(self):
        client = GuardrailsClient("api_key")
        guardrail_id = "grd_testId"
        role = "user"
        text = "Test output"

        # Call the method and raise an exception to simulate a transport/http error other than from the backend
        # e.g., connection error, timeout, etc.
        client.check_text = MagicMock(side_effect=Exception("Transport error"))

        with self.assertRaises(Exception):
            result = client.check_text(
                text=text,
                params={"guardrail_id": guardrail_id, "role": role},
            )

            # Assertions
            self.assertIsInstance(result, GuardrailCheckResponse)
            self.assertEqual(result.check.id, "check_123")
            self.assertFalse(result.passed)
            self.assertFalse(result.failed)
            self.assertTrue(result.errored)
            self.assertIsNotNone(result.error)
            self.assertIsInstance(result.error, Exception)
