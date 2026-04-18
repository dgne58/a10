---
title: "LLM Semantic Router: Intelligent request routing for large language models"
source: "https://developers.redhat.com/articles/2025/05/20/llm-semantic-router-intelligent-request-routing"
author:
  - "[[Ron Haberman]]"
  - "[[Huamin Chen]]"
  - "[[Ricardo Noriega De Soto]]"
  - "[[Andre Fredette]]"
  - "[[David Brewster]]"
  - "[[Shane Utt]]"
  - "[[Christopher Ferreira]]"
published: 2025-05-20
created: 2026-04-13
description: "LLM Semantic Router uses semantic understanding and caching to boost performance, cut costs, and enable efficient inference with llm-d."
tags:
  - "clippings"
---
Today Red Hat announced project llm-d, a new distributed inference platform built to support our vision for an open source AI future. With llm-d, Red Hat and our ecosystem partners enable the vLLM platform to be distributed with prefill/decode disaggregation and KV cache awareness. We have introduced efficient KV cache management and synchronization. But this is just the beginning.

To create an efficient inference engine, smart routing is needed. In the coming weeks and months, we will introduce many enhancements, including LoRA aware routing, auto-scaling enabled routing, xPyD awareness in routing with dynamic resource management triggered from the router, and many more.

Beyond general-purpose LLMs

## Beyond general-purpose LLMs

Today's AI environment is experiencing a surge in specialized large language models (LLMs), each of them possessing its own abilities and strengths. Some possess the ability to reason and do mathematics, others with creative writing skills, and yet others with expertise in domain knowledge.

Yet most applications resort to a "one-size-fits-all" approach, routing all user requests to a general-purpose model, squandering an opportunity for improved performance, cost, and user experience. Ideally, requests should be routed to the best model for the specific task, making effective use of different, usually specialized, models to handle different tasks based on their capabilities.

Furthermore, users often prompt for similar if not identical information, but use different ways to describe the information they seek. Such semantic similarity, once identified by advanced NLP techniques, can be served by cached results to reduce inference latency and cost.

Use cases

## Use cases

The LLM Semantic Router provides a structured solution to this challenge. It intelligently directs incoming requests to the most appropriate LLMs in a managed pool, with a focus on the semantic features of the request content.

LLM Semantic Router enables:

- **Better performance:** The Router examines the request content and directs math problems to math-specialized models, creative work to models that are specialized in writing, and so on.
- **Cost savings:** Direct simpler queries to smaller, lower-cost models using lower cost hardware that is capable of processing simpler requests.
- **Semantic caching:** Cache query responses for semantically similar queries to conserve hardware resources and make responses lightning fast.
- **Prompt guard:** Detect Personal Identification Information (PII) in the request content, and redirect, redact, or reject the request to protect sensitive information from going to public models.

The LLM Semantic Router introduces several key innovations, including semantic understanding, semantic caching, and Envoy External Processor integration.

### Semantic understanding with BERT

The router uses BERT models to understand the semantic meaning of an incoming request, in the following sequence:

1. The Envoy gateway with the semantic processor ExtProc receives user requests for LLM inference service.
2. The semantic processor retrieves the user prompt from the request.
3. The semantic processor converts the prompt into embeddings (numerical vector representations) using the BERT model that is specified in the configuration.
4. The embeddings are compared to the task vectors to identify the nature of the task.
5. The LLM model that is associated with the task is selected to serve this user request.

### Semantic caching

LLM Semantic Router enables an extensible caching system that:

- Stores responses based on semantic similarity.
- Identifies when a new query is semantically similar to a previously seen one.
- Returns cached responses for similar queries, reducing latency and eliminating unneeded use of back-end hardware.

### Integration via Envoy External Processor

The router operates as an Envoy External Processor (ExtProc) filter, allowing it to:

- Intercept incoming API requests.
- Examine and modify both requests and responses.
- Make routing decisions without modifying client code (see Figure 1).
![Flowchart showing client request routing through Envoy Proxy and Semantic Router to different models based on embeddings.](https://developers.redhat.com/sites/default/files/image2_80.png.webp)

Figure 1: How semantic processors classify inference requests and choose the best LLM model.

High-performance Rust + Golang implementation

## High-performance Rust + Golang implementation

Implementing semantic processing in Envoy ExtProc for high performance and wide ecosystem adoption is challenging in the following ways:

- Most of the Envoy ExtProc projects are written in Golang. However, Golang has limited natural language processing (NLP) capabilities.
- Though having a rich ecosystem in NLP and LLM, Python is intrinsically not as efficient as Golang in intensive data processing use cases.

To bridge the gap between these two ecosystems, we choose a new architecture to use Rust and Golang. This architecture leverages:

- Rust Candle Library: Provides efficient BERT embedding generation and similarity matching and text classification.
- Go FFI Bindings: Allow Golang programs to call the Rust functions directly
- Golang based ExtProc Server: Handles the communication with Envoy
Technical walkthrough

## Technical walkthrough

We are pleased to share that our Envoy ExtProc based semantic processor, implemented in the hybrid Rust + Golang approach, is capable of selecting the best LLM model for the prompt and reusing cached responses to serve semantically similar requests.

You can get more details and follow our progress in this [GitHub repository](https://github.com/redhat-et/semantic_router).

### System architecture

The complete system consists of several interconnected components, as shown in Figure 2.

![Sequence diagram illustrating an OpenAI API request flowing through an LLM Router for semantic analysis and routing to an LLM back end.](https://developers.redhat.com/sites/default/files/image1_115.png.webp)

Figure 2: Semantic Processor architecture: How the Semantic Router analyzes, routes, and cache inference requests.

### Request flow

Here's how a request flows through the system:

1. The client sends an OpenAI-compatible API request to the Envoy proxy.
2. Envoy forwards the request to the ExtProc filter (Semantic Processing LLM Router).
3. The router:
	1. Extracts the query from the request.
		2. Checks the semantic cache for similar previous queries.
		3. If not found in cache, generates embeddings and compares with task descriptions.
		4. Determines the most appropriate model.
		5. Modifies the request to target the selected model.
4. Envoy forwards the modified request to the appropriate model backend to improve user experience, performance, and privacy protection.
5. The response flows back through Envoy back to the client.
6. Throughout the entire process, Prometheus metrics are created to track the model selection, semantic cache hit ratio, the HTTP request processing latency, and token usage.

### Monitoring and metrics

The router provides the following Prometheus metrics for observability and Grafana dashboard for visualization:

- Request count by model
- Model Routing decisions and modifications
- Cache hit rates
- Response latencies
- Token usage

These metrics allow AI engineers to better track the performance across distributed inference, so they can understand and optimize to achieve desired service level objectives (SLOs)

Future integration with Gateway API Inference Extension

## Future integration with Gateway API Inference Extension

The LLM Semantic Router integrates with Kubernetes Gateway API Inference Extension (GIE), which extends the Kubernetes Gateway API with intelligent routing capabilities for AI/ML inference workloads.

Integration opportunities include the following:

- Endpoint Picker Proxy (EPP) enhancement:
	- The semantic routing capabilities enhance the EPP's scheduling system.
		- Adding semantic understanding would complement GIE's existing queue and KV-cache awareness.
- Body-based routing:
	- GIE already has a specialized component for body-based routing called Body Based Routing (BBR).
		- The LLM Semantic Router's BERT embedding approach could enhance this capability with deeper semantic understanding.

### Next steps

We have presented our work and [proposal](https://github.com/kubernetes-sigs/gateway-api-inference-extension/issues/770) to the GIE community and received positive feedback. We hope more community interests and participation in this project to enhance the overall LLM inference experience in production.

Conclusion

## Conclusion

The Semantic Router for LLM is an extensible solution for routing requests to the correct model. Through BERT embedding's semantic understanding strength and Envoy ExtProc flexibility, it increases LLM deployment efficiency, performance, and cost economics.

With the growing ecosystem of specialized AI models, smart routing is that much more important. Integration with the Gateway API Inference Extension is an emerging development that would take semantic routing strength to Kubernetes and OpenShift-based AI/ML infrastructure and will enable even more efficient AI inference capabilities using llm-d.

### References

Auto model routing is also seen on platforms such as [OpenRouter](https://openrouter.ai/openrouter/auto) and H2O [Model Selection | Routing you to the best LLM](https://h2o.ai/blog/2024/model-selection/), [AI Router](https://airouter.io/), [Find Your Best LLM: Unify Helps Detect the Right LLM Quickly and Cost-Efficiently](https://community.intel.com/t5/Blogs/Tech-Innovation/Artificial-Intelligence-AI/Find-Your-Best-LLM-Unify-Helps-Detect-the-Right-LLM-Quickly-and/post/1622214), [LLM Routing: Optimize AI Costs Without Sacrificing Quality](https://blog.premai.io/llm-routing-ai-costs-optimisation-without-sacrificing-quality/).

*Last updated: May 28, 2025*