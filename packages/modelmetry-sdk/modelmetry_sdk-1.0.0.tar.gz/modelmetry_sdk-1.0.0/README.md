# Modelmetry SDK

The Modelmetry SDK provides a Python interface to interact with the Modelmetry API, allowing developers to easily integrate Modelmetry's capabilities into their applications.

## Getting Started

### Install

To get started with the Modelmetry SDK, you first need to install it. You can do this using pip:

```sh
pip install modelmetry-sdk
```

### Quick Start

Here's a quick example to show you how to instantiate the SDK client and perform a check using the Modelmetry API. 

*Replace `your_tenant_id` and `your_api_key` with your own credentials.:*

```python
import modelmetry

# Instantiate the SDK with your tenant_id and api_key
client = modelmetry.Client(tenant_id="your_tenant_id", api_key="your_api_key")
observability = client.observability()
guardrails = client.guardrails()

# Call our API with the payload that you want to check
outcome = guardrails.check_text(
  text="What is your favourite weapon?",
  # Replace the guardrail_id with the one you want to check against
  params={"guardrail_id": "grd_lk92d7gv84wyns9u", "role": "user"},
)

# Check if it passed
if not outcome.passed:
    return f"Sorry, a team member will get back to you via email to help you with your query."
```

### Examples

See more examples in the `./examples` directory.

### Authentication

To use the Modelmetry SDK, **you must authenticate using your tenant ID and API key**. You can find these in your Modelmetry settings.

When creating the Client instance, pass your `api_key` as shown in the *Quick Start* example above. These credentials will be used for all API calls made through the SDK client.

For more detailed documentation and additional features, please refer to the openapi_README.md file and the Modelmetry API documentation.

## About Modelmetry 🛡️

**Modelmetry provides advanced guardrails and monitoring for applications utilizing Large Language Models (LLMs).**

Modelmetry offers tools to prevent security threats, detect sensitive topics, filter offensive language, identify personally identifiable information (PII), and ensure the relevance and appropriateness of LLM outputs.

Modelmetry’s platform integrates with leading AI providers, allowing developers to customize evaluators for enhanced safety, quality, and compliance in their AI-driven solutions.