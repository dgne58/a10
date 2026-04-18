---
title: "Quick Start Guide — TensorRT LLM"
source: "https://nvidia.github.io/TensorRT-LLM/quick-start-guide.html"
author:
published:
created: 2026-04-15
description:
tags:
  - "clippings"
---
## Quick Start Guide

This is the starting point to try out TensorRT LLM. Specifically, this Quick Start Guide enables you to quickly get set up and send HTTP requests using TensorRT LLM.

## Launch Docker Container

The [TensorRT LLM container](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tensorrt-llm/containers/release/tags) maintained by NVIDIA contains all of the required dependencies pre-installed. You can start the container on a machine with NVIDIA GPUs via:

```bash
docker run --rm -it --ipc host --gpus all --ulimit memlock=-1 --ulimit stack=67108864 -p 8000:8000 nvcr.io/nvidia/tensorrt-llm/release:1.3.0rc11
```

## Deploy Online Serving with trtllm-serve

You can use the `trtllm-serve` command to start an OpenAI compatible server to interact with a model. To start the server, you can run a command like the following example inside a Docker container:

```bash
trtllm-serve "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
```

You may also deploy pre-quantized models to improve performance. Ensure your GPU supports FP8 quantization before running the following:

```bash
trtllm-serve "nvidia/Qwen3-8B-FP8"
```

For more options, browse the full [collection of generative models](https://huggingface.co/collections/nvidia/inference-optimized-checkpoints-with-model-optimizer) that have been quantized and optimized for inference with the TensorRT Model Optimizer.

Note

If you are running `trtllm-serve` inside a Docker container, you have two options for sending API requests:

1. Expose a port (e.g., 8000) to allow external access to the server from outside the container.
2. Open a new terminal and use the following command to directly attach to the running container:

```bash
docker exec -it <container_id> bash
```

After the server has started, you can access well-known OpenAI endpoints such as `v1/chat/completions`. Inference can then be performed using examples similar to the one provided below, from a separate terminal.

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d '{
        "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "messages":[{"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Where is New York? Tell me in a single sentence."}],
        "max_tokens": 32,
        "temperature": 0
    }'
```

*Example Output*

```json
{
  "id": "chatcmpl-ef648e7489c040679d87ed12db5d3214",
  "object": "chat.completion",
  "created": 1741966075,
  "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "New York is a city in the northeastern United States, located on the eastern coast of the state of New York.",
        "tool_calls": []
      },
      "logprobs": null,
      "finish_reason": "stop",
      "stop_reason": null
    }
  ],
  "usage": {
    "prompt_tokens": 43,
    "total_tokens": 69,
    "completion_tokens": 26
  }
}
```

For detailed examples and command syntax, refer to the [trtllm-serve](https://nvidia.github.io/TensorRT-LLM/commands/trtllm-serve/trtllm-serve.html) section.

Note

Pre-configured settings for deploying popular models with `trtllm-serve` can be found in our [deployment guides](https://nvidia.github.io/TensorRT-LLM/deployment-guide/index.html).

## Run Offline Inference with LLM API

The LLM API is a Python API designed to facilitate setup and inference with TensorRT LLM directly within Python. It enables model optimization by simply specifying a HuggingFace repository name or a model checkpoint. The LLM API streamlines the process by managing model loading, optimization, and inference, all through a single `LLM` instance.

Here is a simple example to show how to use the LLM API with TinyLlama.

```python
1
from tensorrt_llm import LLM, SamplingParams
 2

 3

 4
def main():
 5

 6
    # Model could accept HF model name, a path to local HF model,
 7
    # or Model Optimizer's quantized checkpoints like nvidia/Llama-3.1-8B-Instruct-FP8 on HF.
 8
    llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
 9

10
    # Sample prompts.
11
    prompts = [
12
        "Hello, my name is",
13
        "The capital of France is",
14
        "The future of AI is",
15
    ]
16

17
    # Create a sampling params.
18
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
19

20
    for output in llm.generate(prompts, sampling_params):
21
        print(
22
            f"Prompt: {output.prompt!r}, Generated text: {output.outputs[0].text!r}"
23
        )
24

25
    # Got output like
26
    # Prompt: 'Hello, my name is', Generated text: '\n\nJane Smith. I am a student pursuing my degree in Computer Science at [university]. I enjoy learning new things, especially technology and programming'
27
    # Prompt: 'The president of the United States is', Generated text: 'likely to nominate a new Supreme Court justice to fill the seat vacated by the death of Antonin Scalia. The Senate should vote to confirm the'
28
    # Prompt: 'The capital of France is', Generated text: 'Paris.'
29
    # Prompt: 'The future of AI is', Generated text: 'an exciting time for us. We are constantly researching, developing, and improving our platform to create the most advanced and efficient model available. We are'
30

31

32
if __name__ == '__main__':
33
    main()
```

You can also directly load pre-quantized models [quantized checkpoints on Hugging Face](https://huggingface.co/collections/nvidia/model-optimizer-66aa84f7966b3150262481a4) in the LLM constructor. To learn more about the LLM API, check out the [LLM API Introduction](https://nvidia.github.io/TensorRT-LLM/llm-api/index.html) and [LLM Examples](https://nvidia.github.io/TensorRT-LLM/examples/llm_api_examples.html).

## Run Offline Inference with VisualGen API

The VisualGen API provides a similar interface for diffusion-based image and video generation. Here is a simple example to generate a video with Wan 2.1.

```python
1
#! /usr/bin/env python
 2
# SPDX-FileCopyrightText: Copyright (c) 2022-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
 3
# SPDX-License-Identifier: Apache-2.0
 4

 5
from tensorrt_llm import VisualGen, VisualGenParams
 6
from tensorrt_llm.serve.media_storage import MediaStorage
 7

 8

 9
def main():
10
    visual_gen = VisualGen(model_path="Wan-AI/Wan2.1-T2V-1.3B-Diffusers")
11
    params = VisualGenParams(
12
        height=480,
13
        width=832,
14
        num_frames=81,
15
        guidance_scale=5.0,
16
        num_inference_steps=50,
17
        seed=42,
18
    )
19
    output = visual_gen.generate(
20
        inputs="A cat sitting on a windowsill",
21
        params=params,
22
    )
23
    MediaStorage.save_video(output.video, "output.avi", frame_rate=params.frame_rate)
24

25

26
if __name__ == "__main__":
27
    main()
```

To learn more about VisualGen, check out the [Visual Generation](https://nvidia.github.io/TensorRT-LLM/models/visual-generation.html) documentation and [`examples/visual_gen/`](https://github.com/NVIDIA/TensorRT-LLM/tree/main/examples/visual_gen).