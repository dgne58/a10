---
title: "LLM Router Blueprint by NVIDIA"
source: "https://build.nvidia.com/nvidia/llm-router"
author:
published:
created: 2026-04-13
description: "Route LLM requests to the best model for the task at hand."
tags:
  - "clippings"
---
![](https://build.nvidia.com/_next/image?url=https%3A%2F%2Fassets.ngc.nvidia.com%2Fproducts%2Fapi-catalog%2Fimages%2Fllm-router.jpg&w=3840&q=75)

## LLM Router

Route LLM requests to the best model for the task at hand.

AI systems often face a trade-off between accuracy, latency, and cost. Complex reasoning or multimodal queries need powerful models, but routing every request through the same large model wastes compute and increases response times. Simpler queries don’t need that level of reasoning or visual understanding.

This developer example makes model selection dynamic and data-driven. It supports both text and image inputs and offers two main strategies:

- Intent-based routing that uses smaller language models to interpret query semantics.
- Auto-routing that leverages CLIP embeddings and trained neural networks to optimize routing based on patterns in real data.

By evaluating each request’s complexity, modality, and intent in real time, the router can send lightweight queries to fast, efficient models and reserve high-capacity models for tasks that actually need them. The result is a system that maintains strong performance while reducing unnecessary compute costs.

## Architecture Diagram

[![](https://assets.ngc.nvidia.com/products/api-catalog/llm-router/diagram.jpg)](https://assets.ngc.nvidia.com/products/api-catalog/llm-router/diagram.jpg)

## What’s Included in the Blueprint

### Key Features

This developer example includes architectural diagrams, Docker-based deployment configurations, Jupyter notebooks for exploration and training, and complete source code for local deployment and customization. The LLM Router example supports the following key features and components:

- **Multimodal Router Backend:** Built with [NVIDIA NeMo Agent Toolkit](https://developer.nvidia.com/nemo-agent-toolkit) with FastAPI, supporting both text and image inputs through OpenAI-compatible chat completions API.
- **Two Routing Strategies:** Intent-based routing using Qwen 1.7B for semantic classification, and auto-routing using CLIP embeddings with trained neural networks for optimization.
- **Model Recommendation Engine:** Returns optimal model names rather than proxying requests, providing flexible integration patterns.
- **Interactive Demo Application:** Gradio-based web interface demonstrating end-to-end routing and model calling workflows.
- **Training Pipeline:** Complete notebooks and scripts for training custom neural network routers on your specific data and requirements.
- **Docker Compose Profiles:** Simplified deployment with separate profiles for intent-based and neural network routing strategies.
- **Flexible Model Integration:** Pre-configured for NVIDIA Build API, Azure OpenAI, and standard OpenAI endpoints with easy customization for other providers.

## Software Used in This Blueprint

**NVIDIA NIM™ microservices and Nemotron Models**

- [Llama 3.1 8B Instruct](https://build.nvidia.com/meta/llama-3_1-8b-instruct)
- [Llama 3.1 70B Instruct](https://build.nvidia.com/meta/llama-3_1-70b-instruct)
- [Mixtral 8x22B Instruct](https://build.nvidia.com/mistralai/mixtral-8x22b-instruct)
- [DeepSeek R1](https://build.nvidia.com/deepseek-ai/deepseek-r1)
- [Nemotron Nano 12B VL](https://build.nvidia.com/nvidia/nemotron-nano-12b-v2-vl) - Multimodal reasoning and image understanding
- [Nemotron Nano 9B](https://build.nvidia.com/nvidia/nvidia-nemotron-nano-9b-v2) - Efficient text processing and conversation

**External Models**

- [Qwen 3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B) (vllm) - Intent classification for routing decisions
- [GPT-5 Chat](https://platform.openai.com/) (via Azure OpenAI or OpenAI API) - Complex reasoning and sophisticated analysis
- [CLIP](https://openai.com/research/clip) - Multimodal embeddings for neural network routing

**Infrastructure**

- [NVIDIA Triton Inference Server](https://developer.nvidia.com/triton-inference-server)
- [NVIDIA NeMo Agent Toolkit](https://developer.nvidia.com/nemo) - Router backend framework
- [vLLM](https://vllm.ai/) - High-performance LLM serving for Qwen models
- [CLIP-as-Service](https://clip-as-service.jina.ai/) - CLIP embedding server for neural network routing

## Minimum System Requirements

### Hardware Requirements

- Any NVIDIA GPU with an architecture newer than Volta™ (V100), such as Turing™ (T4), Ampere™ (A100, RTX 30 series), Hopper™ (H100), or later.
- Minimum 16GB GPU memory for Qwen 1.7B model serving
- Additional 8GB GPU memory if using neural network routing with CLIP

### Software Requirements

- Linux operating systems (Ubuntu 22.04 or later recommended) or macOS
- [Git LFS](https://git-lfs.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- NVIDIA API key from [build.nvidia.com](http://build.nvidia.com/) (see [instructions](https://docs.nvidia.com/nim/large-language-models/latest/getting-started.html#option-1-from-api-catalog))
- Python 3.12+ and uv package manager (for local development)
- Azure OpenAI API access or standard OpenAI API key for GPT-5 Chat model

## Ethical Considerations

NVIDIA believes trustworthy AI is a shared responsibility, and we have established policies and practices to enable development for a wide array of AI applications. When downloaded or used in accordance with our terms of service, developers should work with their supporting model team to ensure the models meet requirements for the relevant industry and use case and address unforeseen product misuse. For more detailed information on ethical considerations for the models, please see the Model Card++ Explainability, Bias, Safety and Security, and Privacy Subcards. Please report security vulnerabilities or NVIDIA AI concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## License

Use of the models in this blueprint is governed by the [NVIDIA AI Foundation Models Community License](https://docs.nvidia.com/ai-foundation-models-community-license.pdf).

## Terms of Use

GOVERNING TERMS: The software is governed by the [NVIDIA Software License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-software-license-agreement/) and [Product-Specific Terms for NVIDIA AI Products](https://www.nvidia.com/en-us/agreements/enterprise-software/product-specific-terms-for-ai-products/). Use of the Complexity and Task Qualifier model is governed by the [NVIDIA Open Model License Agreement](https://developer.download.nvidia.com/licenses/nvidia-open-model-license-agreement-june-2024.pdf). Additional Information: [MIT License](https://github.com/microsoft/DeBERTa/blob/master/LICENSE).

#### Meta Llama 3.1 8B, Llama 3.1 70B Instruct

GOVERNING TERMS: The NIM container is governed by the [NVIDIA Software License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-software-license-agreement/) and the [Product Specific Terms for AI Products](https://www.nvidia.com/en-us/agreements/enterprise-software/product-specific-terms-for-ai-products/);

#### Mixtral 8x22B Instruct

GOVERNING TERMS: The NIM container is governed by the [NVIDIA Software License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-software-license-agreement/) and the [Product Specific Terms for AI Products](https://www.nvidia.com/en-us/agreements/enterprise-software/product-specific-terms-for-ai-products/);

#### DeepSeek R1

GOVERNING TERMS: The NIM container is governed by the [NVIDIA Software License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-software-license-agreement/) and the [Product Specific Terms for AI Products](https://www.nvidia.com/en-us/agreements/enterprise-software/product-specific-terms-for-ai-products/);

Use of these model is governed by the [NVIDIA AI Foundation Models Community License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-ai-foundation-models-community-license-agreement/#:~:text=This%20license%20agreement%20\(%E2%80%9CAgreement%E2%80%9D,algorithms%2C%20parameters%2C%20configuration%20files%2C). ADDITIONAL INFORMATION: Llama 3.1 Community License Agreement, Built with Llama;