---
title: "Supported AI Providers | Envoy AI Gateway"
source: "https://aigateway.envoyproxy.io/docs/capabilities/llm-integrations/supported-providers/"
author:
published:
created: 2026-04-13
description: "Since the Envoy AI Gateway is designed to provide a Unified API for routing and managing LLM/AI traffic, it supports various AI providers out of the box."
tags:
  - "clippings"
---
Version: latest

Since the Envoy AI Gateway is designed to provide a Unified API for routing and managing LLM/AI traffic, it supports various AI providers out of the box. A "support of provider" means two things: the API schema support and the Authentication support.  
The former can be configured in the `AIServiceBackend` resource's `schema` field, while the latter is configured in the `BackendSecurityPolicy`.

Below is a table of currently supported providers and their respective configurations.

| Provider Name | API Schema Config on [AIServiceBackend](https://aigateway.envoyproxy.io/docs/api/#aiservicebackendspec) | Upstream Authentication Config on [BackendSecurityPolicy](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyspec) | Status | Note |
| --- | --- | --- | --- | --- |
| [OpenAI](https://platform.openai.com/docs/api-reference) | `{"name":"OpenAI","prefix":"/v1"}` | [API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyapikey) | ✅ |  |
| [AWS Bedrock](https://docs.aws.amazon.com/bedrock/latest/APIReference/) | `{"name":"AWSBedrock"}` | [AWS Bedrock Credentials](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyawscredentials) | ✅ |  |
| [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference) | `{"name":"AzureOpenAI","version":"2025-01-01-preview"}` or `{"name":"OpenAI", "prefix": "/openai/v1"}` | [Azure Credentials](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyazurecredentials) or [Azure API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyazureapikey) | ✅ |  |
| [Google Gemini on AI Studio](https://ai.google.dev/gemini-api/docs/openai) | `{"name":"OpenAI","prefix":"/v1beta/openai"}` | [API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyapikey) | ✅ | Only the OpenAI compatible endpoint |
| [Google Vertex AI](https://cloud.google.com/vertex-ai/docs/reference/rest) | `{"name":"GCPVertexAI"}` | [GCP Credentials](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicygcpcredentials) | ✅ |  |
| [Anthropic on GCP Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/claude) | `{"name":"GCPAnthropic", "version":"vertex-2023-10-16"}` | [GCP Credentials](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicygcpcredentials) | ✅ | Support both Native Anthropic messages endpoint and OpenAI compatible endpoint |
| [Groq](https://console.groq.com/docs/openai) | `{"name":"OpenAI","prefix":"/openai/v1"}` | [API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyapikey) | ✅ |  |
| [Grok](https://docs.x.ai/docs/api-reference?utm_source=chatgpt.com#chat-completions) | `{"name":"OpenAI","prefix":"/v1"}` | [API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyapikey) | ✅ |  |
| [Together AI](https://docs.together.ai/docs/openai-api-compatibility) | `{"name":"OpenAI","prefix":"/v1"}` | [API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyapikey) | ✅ |  |
| [Cohere](https://docs.cohere.com/v2/docs/compatibility-api) | `{"name":"Cohere","version":"v2"}` or `{"name":"OpenAI","prefix":"/compatibility/v1"}` | [API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyapikey) | ✅ | Supports native Cohere v2 (e.g., /cohere/v2/rerank) and OpenAI-compatible endpoints. |
| [Mistral](https://docs.mistral.ai/api/#tag/chat/operation/chat_completion_v1_chat_completions_post) | `{"name":"OpenAI","prefix":"/v1"}` | [API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyapikey) | ✅ |  |
| [DeepInfra](https://deepinfra.com/docs/inference) | `{"name":"OpenAI","prefix":"/v1/openai"}` | [API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyapikey) | ✅ | Only the OpenAI compatible endpoint |
| [DeepSeek](https://api-docs.deepseek.com/) | `{"name":"OpenAI","prefix":"/v1"}` | [API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyapikey) | ✅ |  |
| [Hunyuan](https://cloud.tencent.com/document/product/1729/111007) | `{"name":"OpenAI","prefix":"/v1"}` | [API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyapikey) | ✅ |  |
| [Tencent LLM Knowledge Engine](https://www.tencentcloud.com/document/product/1255/70381?lang=en) | `{"name":"OpenAI","prefix":"/v1"}` | [API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyapikey) | ✅ |  |
| [Tetrate Agent Router Service (TARS)](https://router.tetrate.ai/) | `{"name":"OpenAI","prefix":"/v1"}` | [API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyapikey) | ✅ |  |
| [SambaNova](https://docs.sambanova.ai/sambastudio/latest/open-ai-api.html) | `{"name":"OpenAI","prefix":"/v1"}` | [API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyapikey) | ✅ |  |
| Self-hosted-models | `{"name":"OpenAI","prefix":"/v1"}` | N/A | ⚠️ | Depending on the API schema spoken by self-hosted servers. For example, [vLLM](https://docs.vllm.ai/en/v0.8.3/serving/openai_compatible_server.html) speaks the OpenAI format. Also, API Key auth can be configured as well. |
| [Anthropic](https://docs.claude.com/en/home) | `{"name":"Anthropic"}` | [Anthropic API Key](https://aigateway.envoyproxy.io/docs/api/#backendsecuritypolicyanthropicapikey) | ✅ | Support only Native Anthropic messages endpoint |